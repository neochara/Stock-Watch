from data_processing import check_null, _count_null
import pandas as pd
import numpy as np

def test_check_null():
    data = {'A': [0, 1, 0, 1],
            'B': [4, 5, np.nan, 9],
            'C': [np.nan, 0, np.nan, np.nan],
            'F': [0, 0, 0, 0]}
    df = pd.DataFrame(data)

    check_null(df,'pop')

def test_count_null():
    df = pd.DataFrame({
        'A': [0, 1, 0, 1],
        'B': [4, 5, np.nan, 9],
        'C': [np.nan, 0, np.nan, np.nan],
        'F': [0, 0, 0, 0]
    })
    expected_result = 4
    actual_result = _count_null(df)

    assert actual_result == expected_result



def main():
   test_count_null()

if __name__ == "__main__":
    main()