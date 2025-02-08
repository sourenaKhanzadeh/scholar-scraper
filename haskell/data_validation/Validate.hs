module Validate where

import Data.Char (isAlphaNum)

validateTitle :: String -> Bool
validateTitle title = not (null title) && all isAlphaNum (filter (/= ' ') title)

validateAuthors :: String -> Bool
validateAuthors authors = not (null authors) && ',' `elem` authors

validateAbstract :: String -> Bool
validateAbstract abstract = length abstract > 20