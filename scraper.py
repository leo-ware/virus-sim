import pandas as pd
import numpy as np
import requests
import io


class DataGetter:
    def __init__(self, country_code=156):
        self.country_code = int(country_code)

    def get_data(self, scale=1000, country_code=None):
        if country_code is None:
            country_code = self.country_code

        response = requests.get("https://www.populationpyramid.net/api/pp/" + str(country_code) + "/2019/?csv=true")
        file_object = io.StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(file_object)

        # Formatting for South China Morning Post tranching and pyramid
        # 0-9, 10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
        df['M'] = -1 * df['M']

        ser = [pd.Series(['0-9', df.M[:2].sum(), df.F[:2].sum()], index=df.columns),
               pd.Series(['10-19', df.M[2:4].sum(), df.F[2:4].sum()], index=df.columns),
               pd.Series(['20-29', df.M[4:6].sum(), df.F[4:6].sum()], index=df.columns),
               pd.Series(['30-39', df.M[6:8].sum(), df.F[6:8].sum()], index=df.columns),
               pd.Series(['40-49', df.M[8:10].sum(), df.F[8:10].sum()], index=df.columns),
               pd.Series(['50-59', df.M[10:12].sum(), df.F[10:12].sum()], index=df.columns),
               pd.Series(['60-69', df.M[12:14].sum(), df.F[12:14].sum()], index=df.columns),
               pd.Series(['70-79', df.M[14:16].sum(), df.F[14:16].sum()], index=df.columns),
               pd.Series(['80+', df.M[16:].sum(), df.F[16:].sum()], index=df.columns)]

        df = df.append(ser, ignore_index=True)
        df = df.drop(df.index[0:21])
        df = df.reset_index(drop=True)

        # numbers based on SCMP reporting and mortality data for each demographic
        # df['infection_rate'] = np.array([0.3,0.3,0.4,0.4,0.3,0.4,0.5,0.6,0.7])/10
        df['mortality_rate'] = np.array([0.01, 0.2, 0.2, 0.2, 0.4, 1.3, 3.6, 8, 14.8])

        df['S0'] = round((((-1 * df['M'] + df['F']) / ((-1 * df['M']).sum() + df['F'].sum())) * scale), 0)
        df['I0'] = [5] * 9
        df['R0'] = np.zeros(len(df['I0']))
        df['D0'] = np.zeros(len(df['I0']))

        df['name'] = df['Age']
        df.set_index("name", inplace=True)

        return df
