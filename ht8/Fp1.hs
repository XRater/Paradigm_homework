module Fp1 where

head' :: [a] -> a
head' [] = undefined
head' (x : xs) = x

tail' :: [a] -> [a]
tail' [] = []
tail' (x : xs) = xs

take' :: Int -> [a] -> [a]
take' 0 x = []
take' a [] = [] -- If not enouth elements return full list
take' a (x : xs) = x : take' (a - 1) xs

drop' :: Int -> [a] -> [a]
drop' 0 x = x
drop' a [] = []
drop' a (x : xs) = drop' (a - 1) xs

filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (x : xs) | f x == True  = x : filter' f xs
filter' f (x : xs) | f x == False = filter' f xs

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f a [] = a
foldl' f a (x : xs) = foldl' f (f a x) xs

concat' :: [a] -> [a] -> [a]
concat' [] [] = []
concat' [] (x : xs) = x : concat' [] xs 
concat' (x : xs) y = x : concat' xs y 

quickSort' :: Ord a =>[a] -> [a]
quickSort' [] = []
quickSort' (x : xs) = concat' (smallpart x xs) (x : (bigpart x (xs))) 
    where
    smallpart x xs = quickSort' (filter' (<=x) xs) 
    bigpart x xs = quickSort' (filter' (>x) xs)   
    
