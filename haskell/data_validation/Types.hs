module Types where

data Paper = Paper {
    title    :: String,
    authors  :: String,
    abstract :: String
} deriving (Show, Eq)