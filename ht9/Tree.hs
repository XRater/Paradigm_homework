import Prelude hiding (lookup)

data BinaryTree k v = Nil | Cons (BinaryTree k v) (k, v) (BinaryTree k v) deriving (Show, Eq)

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
insert k v (Cons x p y) | k == fst p = Cons x (k, v) y
                        | k < fst p  = Cons (insert k v x) p y  
                        | k > fst p  = Cons x p (insert k v y)


delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v
delete k Nil = Nil
delete k (Cons x p y) | k < fst p  = delete k x
                      | k > fst p  = delete k y
                      | k == fst p = mergeSorted x y 
    where
        mergeSorted Nil x = x
        mergeSorted (Cons x p y) r = Cons (mergeSorted x y) p r
