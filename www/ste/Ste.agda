-- A small ASD-STE100 (Simplified Technical English) check of English Markdown, in Agda.
-- It checks two writing rules of ASD-STE100 and a sample of words that the STE dictionary does
-- not approve; it is not the dictionary. A finding prints as file:line: rule: detail, and the
-- program exits 1. Usage: ste FILE...   (`just ste`)
--
--   sentence   a descriptive sentence has 25 words or fewer (rule 5.1)
--   paragraph  a paragraph has 6 sentences or fewer (rule 6.6)
--   word       a word of the sample below is replaced by its approved word
module Ste where

open import Data.Bool using (Bool; true; false; if_then_else_; _∧_; _∨_; not)
open import Data.Char as Char using (Char)
open import Data.List as List using (List; []; _∷_; length; map; concatMap; filterᵇ; reverse; take; drop)
open import Data.Bool.ListAction using (any)
open import Data.Maybe using (Maybe; just; nothing)
open import Data.Nat using (ℕ; zero; suc; _<ᵇ_; _+_)
open import Data.Nat.Show using (show)
open import Data.Product using (_×_; _,_)
open import Data.String as String using (String; fromList; toList; _++_)
  renaming (_==_ to _≈_)
open import Data.Unit using (⊤; tt)
open import Function using (_∘_; case_of_)
open import IO using (IO; Main; run; _>>=_; _>>_; pure; putStrLn; readFiniteFile)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import System.Environment using (getArgs)
open import System.Exit using (exitFailure)

maxWords maxSentences : ℕ
maxWords = 25
maxSentences = 6

-- The sample: a word that the dictionary does not approve, and the approved word to write.
unapproved : List (String × String)
unapproved =
  ("utilize" , "use") ∷ ("utilise" , "use") ∷ ("approximately" , "about") ∷
  ("commence" , "start") ∷ ("terminate" , "stop") ∷ ("numerous" , "many") ∷
  ("sufficient" , "enough") ∷ ("subsequently" , "then") ∷ ("facilitate" , "help") ∷
  ("prior" , "before") ∷ []

------------------------------------------------------------------------
-- Words and sentences

-- [text](url) becomes text: a URL is not a word.
unlink : List Char → List Char
unlink [] = []
unlink (']' ∷ '(' ∷ cs) = skip cs
  where
  skip : List Char → List Char
  skip [] = []
  skip (')' ∷ rest) = unlink rest
  skip (_ ∷ rest) = skip rest
unlink ('[' ∷ cs) = unlink cs
unlink (']' ∷ cs) = unlink cs
unlink (c ∷ cs) = c ∷ unlink cs

hasLetter : String → Bool
hasLetter = any Char.isAlpha ∘ toList

endsSentence : String → Bool
endsSentence w with reverse (toList w)
... | '.' ∷ _ = true
... | '?' ∷ _ = true
... | '!' ∷ _ = true
... | _ = false

-- The words of a paragraph, cut into sentences after a word that ends with . ? or !
sentences : List String → List (List String)
sentences = go []
  where
  go : List String → List String → List (List String)
  go acc [] = if 0 <ᵇ length acc then reverse acc ∷ [] else []
  go acc (w ∷ ws) = if endsSentence w then reverse (w ∷ acc) ∷ go [] ws else go (w ∷ acc) ws

wordCount : List String → ℕ
wordCount = length ∘ filterᵇ hasLetter

bare : String → String
bare = fromList ∘ map Char.toLower ∘ filterᵇ Char.isAlpha ∘ toList

------------------------------------------------------------------------
-- Paragraphs. A blank line, a heading, a list item and a quote line start a new one. The front
-- matter (from a first line --- to the next ---) and the headings are not prose.

starts : String → String → Bool
starts p s = p ≈ fromList (take (length (toList p)) (toList s))

numbered : List String → List (ℕ × String)
numbered = go 1
  where
  go : ℕ → List String → List (ℕ × String)
  go _ [] = []
  go n (l ∷ ls) = (n , l) ∷ go (suc n) ls

-- Drop the front matter, keep the line numbers of the file.
body : List (ℕ × String) → List (ℕ × String)
body ((_ , "---") ∷ ls) = after ls
  where
  after : List (ℕ × String) → List (ℕ × String)
  after [] = []
  after ((_ , "---") ∷ rest) = rest
  after (_ ∷ rest) = after rest
body ls = ls

record Para : Set where
  constructor para
  field
    line  : ℕ
    words : List String

wordsOf : String → List String
wordsOf l = String.words (fromList (unlink (toList (strip l))))
  where
  strip : String → String
  strip s = if starts "- " s ∨ starts "> " s then fromList (drop 2 (toList s)) else s

paragraphs : List (ℕ × String) → List Para
paragraphs = go nothing
  where
  close : Maybe Para → List Para → List Para
  close nothing ps = ps
  close (just p) ps = p ∷ ps

  go : Maybe Para → List (ℕ × String) → List Para
  go cur [] = close cur []
  go cur ((n , l) ∷ ls) =
    if not (hasLetter l) ∨ starts "#" l then close cur (go nothing ls)
    else if starts "- " l ∨ starts "> " l then close cur (go (just (para n (wordsOf l))) ls)
    else go (more cur) ls
    where
    more : Maybe Para → Maybe Para
    more nothing = just (para n (wordsOf l))
    more (just (para m ws)) = just (para m (ws List.++ wordsOf l))

------------------------------------------------------------------------
-- Findings

record Finding : Set where
  constructor finding
  field
    line   : ℕ
    rule   : String
    detail : String

lookup : String → List (String × String) → Maybe String
lookup _ [] = nothing
lookup w ((k , v) ∷ kvs) = if w ≈ k then just v else lookup w kvs

checkPara : Para → List Finding
checkPara (para n ws) = List.concat (long ∷ many ∷ concatMap word ws ∷ [])
  where
  ss = sentences ws
  long = concatMap (λ s → let k = wordCount s in
           if maxWords <ᵇ k then finding n "sentence" (show k ++ " words, at most 25") ∷ [] else []) ss
  many = if maxSentences <ᵇ length ss
         then finding n "paragraph" (show (length ss) ++ " sentences, at most 6") ∷ [] else []
  word : String → List Finding
  word w with lookup (bare w) unapproved
  ... | just v  = finding n "word" ("\"" ++ bare w ++ "\" is not approved, write \"" ++ v ++ "\"") ∷ []
  ... | nothing = []

check : String → List Finding
check = concatMap checkPara ∘ paragraphs ∘ body ∘ numbered ∘ String.lines

-- An empty text has no finding, and the rule of length holds at its edge.
empty : check "" ≡ []
empty = refl

edge : check "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four twenty-five." ≡ []
edge = refl

over : length (check "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twenty-one twenty-two twenty-three twenty-four twenty-five twenty-six.") ≡ 1
over = refl

word-sample : length (check "We utilize it.") ≡ 1
word-sample = refl

------------------------------------------------------------------------
-- The program

report : String → Finding → String
report file (finding n r d) = file ++ ":" ++ show n ++ ": " ++ r ++ ": " ++ d

checkFiles : List String → IO ℕ
checkFiles [] = pure 0
checkFiles (f ∷ fs) = do
  text ← readFiniteFile f
  let found = check text
  printAll (map (report f) found)
  rest ← checkFiles fs
  pure (length found + rest)
  where
  printAll : List String → IO ⊤
  printAll [] = pure tt
  printAll (s ∷ ss) = putStrLn s >> printAll ss

main : Main
main = run do
  files ← getArgs
  n ← checkFiles files
  if 0 <ᵇ n
    then (putStrLn ("ste: " ++ show n ++ " findings") >> exitFailure)
    else putStrLn ("ste: " ++ show (length files) ++ " files, no finding")
