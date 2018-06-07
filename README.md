# Lab6CSC466
## Dmitriy Timokhin ~ Hanson Egbert

## Running the program
    -EvaluateCFList.py
        python EvaluateCFlist.py <method> <testing file>
        ex: python EvaluateCFList.py 1 testing_list.txt
        
        Note: the methods are as follows ->
            1: Mean Utility
            2: Average weighted sum
            3: Average weighted Nnn sum
        Note: The format of the testing file must be as follows ->
        ex:
            0, 1
            1, 4
            10, 50
        This means we are predicting user 0 item 1 .. etc.
    -EvaluateCFRandom.py
        python EvaluateCFRandom.py <method> <# of predictions> <# of tests>
        ex: python EvaluateCFRandom.py 1 30 8
        
        Here method is the same as stated above.
        <# of prediction> : The number of predictions per test
        <# of tests> : The number of tests to be run with the specified number of predictions
    
    
    Note: 
        distance_items.txt represents a distance matrix for the pearson coefficients between items.