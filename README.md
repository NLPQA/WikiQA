# WikiQA

What problems still exist in ask pipeline?

1) Need to improve the way to pass sentence to different module.
> * We pass sentence to each module by calling "contains_*" function, which sometimes cause error
> * For example, in the function "contains_name", sentence in which any word tagged by "PERSON" will be sent to who module instead of what module, even though sometimes the word tagged by "PERSON" is not subject of that sentence.

2) Clause
> * Now I think all modules can only handle simple sentences, not sentences with complicated structure, such as clauses involved. This needs to be handled in pre-process.
