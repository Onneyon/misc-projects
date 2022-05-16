{-# OPTIONS_GHC -Wall #-}
module LogAnalysis where
import Log

parseMessage :: String -> LogMessage
parseMessage x = parseMessage' $ words x
    where parseMessage' ("E":en:ts:msg) = LogMessage (Error $ read en) (read ts) $ unwords msg
          parseMessage' ("W":ts:msg) = LogMessage Warning (read ts) $ unwords msg
          parseMessage' ("I":ts:msg) = LogMessage Info (read ts) $ unwords msg
          parseMessage' y = Unknown $ unwords y

parse :: String -> [LogMessage]
parse = map parseMessage . lines

insert :: MessageTree -> LogMessage -> MessageTree
insert tree (Unknown _)                       = tree
insert Leaf msg                               = Node Leaf msg Leaf
insert (Node na nodeMsg nb) msg
    | getTimestamp msg < getTimestamp nodeMsg = Node (insert na msg) nodeMsg nb
    | otherwise                               = Node na nodeMsg (insert nb msg)
        where getTimestamp (LogMessage _ ts _) = ts
              getTimestamp (Unknown _)         = 0
    
build :: [LogMessage] -> MessageTree
build [] = Leaf
build (x:xs) = insert (build xs) x

inOrder :: MessageTree -> [LogMessage]
inOrder Leaf                 = []
inOrder (Node Leaf msg Leaf) = [msg]
inOrder (Node na msg Leaf)   = inOrder na ++ [msg]
inOrder (Node Leaf msg nb)   = inOrder nb ++ [msg]
inOrder (Node na msg nb)     = inOrder na ++ [msg] ++ inOrder nb

whatWentWrong :: [LogMessage] -> [String]
whatWentWrong = map extractContent . inOrder . build . filter filterError
    where extractContent (LogMessage _ _ c) = c
          extractContent (Unknown _)        = ""
          filterError (LogMessage (Error y) _ _) = y >= 50
          filterError _ = False
