
import pandas as pd
import env

# Acquire

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_zillow_data():

    query ='''
    SELECT p_17.parcelid, p_17.logerror, p_17.transactiondate, p.*

    FROM predictions_2017 p_17

    JOIN (SELECT parcelid, Max(transactiondate) as tdate
      
          FROM predictions_2017
        
          GROUP BY parcelid )as sq1

    ON (sq1.parcelid=p_17.parcelid and sq1.tdate = p_17.transactiondate )
    
    LEFT JOIN properties_2017 p 
    ON p_17.parcelid=p.parcelid

    LEFT JOIN storytype
    USING (storytypeid)

    LEFT JOIN airconditioningtype
    USING (airconditioningtypeid)

    LEFT JOIN architecturalstyletype
    USING (architecturalstyletypeid)

    LEFT JOIN buildingclasstype
    USING (buildingclasstypeid)

    LEFT JOIN heatingorsystemtype
    USING (heatingorsystemtypeid)

    LEFT JOIN propertylandusetype
    USING (propertylandusetypeid)

    LEFT JOIN typeconstructiontype
    USING (typeconstructiontypeid)

    WHERE (p.latitude is not null and p.longitude is not null)
    
    AND (unitcnt = 1 or unitcnt = null)
    
    AND (bathroomcnt > 0 and bedroomcnt > 0 and calculatedfinishedsquarefeet > 500)
    
    AND propertylandusedesc in ('Residential General','Single Family Residential', 'Rural Residence', 'Mobile Home', 'Bungalow', 'Manifactured, Modular, Prefabricated Homes', 'Patio Home', 'Inferred Single Family Residential');
    '''
    
    return pd.read_sql(query, get_connection('zillow'))