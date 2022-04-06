import pandas as pd; pd.options.mode.chained_assignment = None
import os; import sys;
import numpy as np
import sklearn
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(1, '/opt/airflow/dags')
os.chdir('/opt/airflow/dags')
import DAL.FlightsDAL as FlightsDAL

# dfMainData = pd.read_csv(f'./BLL/resources/2009.csv')

def calculateDelay(pYear):

    # Crea la tabla delay si no existe
    FlightsDAL.crearTabla()

    if FlightsDAL.verificarExistente(pYear):
        raise Exception('Error: Este año ya fue procesado.')

    print('Loading CSV')
    dfMainData = pd.read_csv(f'./BLL/resources/{pYear}.csv', low_memory=True)
    
    print('Procesing CSV')
    dfDateCounts = dfMainData.groupby([
        'ORIGIN',
        'FL_DATE'
    ], dropna=False, as_index=False).size()

    dfDelays = dfMainData.groupby([
        'ORIGIN',
        'FL_DATE'
    ], dropna=False, as_index=False).agg({
        'DEP_DELAY': np.mean,
    })

    dfResult = pd.merge(dfDateCounts, dfDelays, on=['ORIGIN', 'FL_DATE'], how='inner')


    mOrigins = dfDelays['ORIGIN'].drop_duplicates()
    dfResult = dfResult.fillna(0)

    # Renaming columns
    dfResult.columns = ['ORIGIN', 'FL_DATE', 'AMOUNT', 'DEP_DELAY']

    # Formatting dates for using in the graph
    dfResult['FL_FORMATTED_DATE'] = pd.to_datetime(dfResult['FL_DATE']).dt.strftime("%m%d")

    dfResult['DAY'] = pd.to_datetime(dfResult['FL_DATE']).dt.strftime("%d")
    dfResult['FL_DATE'] = pd.to_datetime(dfResult['FL_DATE']).dt.strftime("%y%m%d")


    dfCalcs = pd.DataFrame()

    # mOrigins = ['ABQ', 'EZE', 'LGW', 'EWR']

    for mOrigin in mOrigins:

        dfFiltered = dfResult[dfResult['ORIGIN'] == mOrigin]

        # Seteamos el numero de muestras según los datos que tenemos
        Samples = 5
        if len(dfFiltered) < Samples:
            Samples = len(dfFiltered)
        
        lof = LocalOutlierFactor(n_neighbors=Samples, leaf_size=7)

        dfFiltered['ANOMALY'] = lof.fit_predict(dfFiltered.drop(['ORIGIN', 'AMOUNT', 'FL_FORMATTED_DATE', 'FL_DATE'], axis=1))

        # Creating a Df with only Anomalies
        dfOnlyAnomaly = dfFiltered[dfFiltered['ANOMALY'] < 1]

        plt.plot(dfFiltered['FL_FORMATTED_DATE'], dfFiltered['DEP_DELAY'])

        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)

        # Show dates only every 30 days
        days = 15
        xticks_pos, xticks_labels = plt.xticks()
        myticks = [j for i,j in enumerate(xticks_pos) if not i%days]
        newlabels = [label for i,label in enumerate(xticks_labels) if not i%days]
        plt.gca().set_xticks(myticks)

        # Creating dots where the anomalies are
        plt.scatter(dfOnlyAnomaly['FL_FORMATTED_DATE'], dfOnlyAnomaly['DEP_DELAY'], c='red')

        plt.title(f"Origin: {mOrigin}")
        plt.xlabel("Date")
        plt.ylabel("Flight Delays")
        
        # Saving the graph
        plt.savefig(fname=f'./BLL/exports/{pYear}/{mOrigin}.jpg', dpi=90)
        plt.clf()

        dfFiltered.loc[dfFiltered['ANOMALY'] > 0, 'ANOMALY'] = False
        dfFiltered.loc[dfFiltered['ANOMALY'] < 0, 'ANOMALY'] = True
        dfFiltered['YEAR'] = pYear

        FlightsDAL.copiarDatos(dfFiltered)

        


