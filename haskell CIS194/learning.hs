import Data.List

doubleMe x = x + x
doubleUs x y = doubleMe x + doubleMe y
doubleSmallNumber x = if x > 100
    then x
    else x*2
-- return a doubled list with only elements that are greater than or equal to 12
doubleList xs = [ x*2 | x <- xs, x*2 >= 12 ]

removeNonUppercase s = [ c | c <- s, c `elem` ['A'..'Z'] ]

quickSort :: (Ord a) => [a] -> [a]
quickSort [] = []
quickSort (x:xs) =
    let smaller = quickSort [ y | y <- xs, y <= x ]
        larger  = quickSort [ y | y <- xs, y > x ]
    in smaller ++ [x] ++ larger

fizzBuzzCheck :: (Integral a, Show a) => a -> String
fizzBuzzCheck x
    | x `mod` 3 == 0 && x `mod` 5 == 0 = "Fizzbuzz"
    | x `mod` 5 == 0 = "Buzz"
    | x `mod` 3 == 0 = "Fizz"
    | otherwise      = show x

fizzBuzz :: (Integral a, Show a) => [a] -> [String]
fizzBuzz [] = []
fizzBuzz xs = map fizzBuzzCheck xs--foldr (\x acc -> fizzBuzzCheck x : acc) [] xs
--fizzBuzz (x:xs)
--    | x `mod` 3 == 0 = 1000 : fizzBuzz xs
--    | x `mod` 5 == 0 = 2000 : fizzBuzz xs
--    | otherwise =         x : fizzBuzz xs

pairToList :: (a, a) -> [a]
pairToList (x,y) = [x,y]

splitSentence :: String -> [String]
splitSentence [] = []
splitSentence xs = let first = takeWhile (/=' ') xs 
                       rest = head (splitSentence ( tail (dropWhile (/=' ') xs) ))
                   in (\x y -> [x, y]) first rest