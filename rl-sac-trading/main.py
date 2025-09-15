from data_manip import prep, indicators, gaf
import numpy as np

def main():
    df = prep() #Prepare the data
    df = indicators(df) # Add technical indicators

    gaf_images, gaf_indices = gaf(df) # generate GAF images
    gaf_images_np = np.array(gaf_images)
    np.save("./GAF/gaf_images.npy", gaf_images_np)

    df_gaf = df.loc[gaf_indices]
    df_gaf.to_csv("./GAF/gaf_features.csv")


if __name__ == "__main__":
    main()