import Prelude hiding (lookup)

data BinaryTree k v = Nil | Cons (BinaryTree k v) (k, v) (BinaryTree k v) deriving Show

treeToList :: BinaryTree k v -> [v]
treeToList Nil = []
treeToList (Cons x p y) = treeToList x ++ [snd p] ++ treeToList y

listToTree :: Ord k => [(k, v)] -> BinaryTree k v
listToTree [] = Nil
listToTree (x : xs) = insert (fst x) (snd x) (listToTree xs)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
lookup k Nil = Nothing
lookup k (Cons x p y) | k < fst p  = lookup k x
                      | k > fst p  = lookup k y                      
                      | k == fst p = Just (snd p)

insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
insert k v Nil = Cons Nil (k, v) Nil
insert k v (Cons x p y) | k < fst p  = Cons (insert k v x) p y  
                        | k > fst p  = Cons x p (insert k v y)
                        | k == fst p = Cons x (k, v) y
 
                      
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Cons x p y) | k < fst p  = Cons (delete k x) p y
                      | k > fst p  = Cons x p (delete k y)
                      | k == fst p = extractRoot x p y 
        
        where
        extractRoot x p Nil = x
        extractRoot x p y = Cons x (getMin y) (extractMin y)            
            
            where
            getMin (Cons Nil p y) = p
            getMin (Cons x p y) = getMin x
            
            extractMin (Cons Nil p y) = y
            extractMin (Cons x p y) = Cons (extractMin x) p y
                

tree1 = Nil
tree2 = insert 4 4 tree1
tree3 = insert 2 2 tree2
tree4 = insert 6 6 tree3
tree5 = insert 3 3 tree4
tree6 = insert 1 1 tree5
tree7 = insert 5 5 tree6
tree8 = insert 7 7 tree7
tree9 = delete 4 tree8

