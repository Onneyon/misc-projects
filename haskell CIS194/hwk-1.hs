toDigits    :: Integer -> [Integer]
toDigitsRev :: Integer -> [Integer]

toDigits x
    | x < 1     = []
    | otherwise = toDigits (x `div` 10) ++ [x `mod` 10]

toDigitsRev x =
    reverse $ toDigits x

doubleEveryOther :: [Integer] -> [Integer]
{-
doubleEveryOther []  = []
doubleEveryOther [x] = [x]
doubleEveryOther xs  =
    doubleEveryOther (init $ init xs) ++ [(*2) . last . init $ xs] ++ [last xs]
-}
doubleEveryOther = reverse . zipWith ($) (concat $ repeat [id, (*2)]) . reverse

sumDigits :: [Integer] -> Integer

sumDigits [] = 0
sumDigits xs =
    sum $ map (sum . toDigits) xs

validate :: Integer -> Bool

validate 0 = False
validate x =
    let vs  = toDigits x
        vsd = map (*2) vs
        s   = sumDigits vsd
    in  (s `mod` 10 == 0)

type Peg = String
type Move = (Peg, Peg)
hanoi :: Integer -> Peg -> Peg -> Peg -> [Move]

hanoi 0 _ _ _ = []
hanoi 1 a b _ = [(a, b)]
hanoi x a b c = -- start, end, temp storage
    let y = x - 1
    in hanoi y a c b ++ hanoi 1 a b c ++ hanoi y c b a

parseHanoi :: [Move] -> [String]

parseHanoi [] = []
parseHanoi xs =
    [ fst x ++ " -> " ++ snd x | x <- xs ]