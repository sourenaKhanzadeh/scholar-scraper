module Main where

import Validate
import Types

validatePaper :: Paper -> Bool
validatePaper (Paper title authors abstract) = 
    validateTitle title && validateAuthors authors && validateAbstract abstract

main :: IO ()
main = do
    let paper = Paper "Reinforcement Learning" "John Doe, Jane Smith" "An introduction to RL."
    if validatePaper paper
        then putStrLn "Paper is valid."
        else putStrLn "Paper is invalid."