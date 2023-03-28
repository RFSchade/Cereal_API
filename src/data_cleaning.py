#=============================================================#
#======================> Data Cleaning <======================#
#=============================================================#

#=====> Import modules
import os
import pandas as pd

#=====> Define main()
def main():
    # > Import data 
    # Filepath 
    filepath = os.path.join("data", "cereal_data.csv")
    # Load 
    df = pd.read_csv(filepath, sep = ";")
    
    # > Drop unimportant stuff
    df = df.drop("rating", axis=1)
    df = df.drop(0, axis=0)
    
    # > Add ID
    df.reset_index(inplace=True)
    df = df.rename(columns={"index": "id"})
    
    # > Save clean data
    outpath = os.path.join("data", "cereal_clean.csv")
    df.to_csv(outpath, index = False) 
    
    # > Print info 
    print("[info] Data is cleaned!")
    
# Run main() function from terminal only
if __name__ == "__main__":
    main()