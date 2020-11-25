# OASIS Segmentation Training Data Generation

## Script 1 Info:
Script one calculates the positions and sizes of islands and stores them as text files. Variables to decide here:
1. numberOfImages: Choose how many images to create
2. minimumIslands: Minimum islands in an image
3. maximumIslands: Maximum islands in an image
4. minimumSize: Minimum size of an island
5. maximumSize: Maximum size of an island

## Script 2 Info:
Script two should be run after script one and renders out 'photorealistic' training data. Variables to decide here:
1. res: Tuple; (x,y) size of rendered image

## Script 3 Info:
Script three should be run after script one and two only after certain changes have been made to the environment. Here you can choose the type of masks you want to generate. Variables to decide here:
1. instanceSegmentation: Change to false if you want separate masks for front and back and true if you want one mask per island.
2. res: Tuple; (x,y) size of rendered mask (SHOULD BE SAME AS SCRIPT 2)

## Script 4 Info:
Script 4 should be run after script one, two and three only. This will split the images and masks into test-train sets. It is designed to run outside of Blender due to certain required packages. No variables to decide here currently.

## Script 5 Info:
Script 5 should be run after script one, two, three and four only. This will add noise and normalise train/test images. This uses a yaml config file which can be changed. It also must be run in a specific way. No varibales to decide here currently.

## Stepwise Usage
1. Open up the attached Blender file. It should be empty.
2. Open Window -> Toggle System Console. You can view the output of the Python scripts here.
3. Click on the 3D Viewport and press Shift+F11 to switch the window to text editor mode.
4. Now you can click 'open' and open up script 1. Make any changes here if required and run the script.
5. The positions and sizes of islands should be saved as text files in the repository directory.
6. Now, back in Blender, open up script 2. Run it. Monitor the System Console until all files are rendered. Clicking the Blender screen will cause it to stop responding so avoid that.
7. Now click on the text editor and press Shift+F5 to switch the window to 3D Viewport.
8. You should see two planes in the environment. Select the one with 'green' in the name using the Outliner on the right. Edit its texture in the menu right below and open emission colour. Switching to RGB, bring the green channel up to 100.
9. Do the same procedure with the plane with 'red' in the name, except bring the red channel in emission to 100.
10. Now you can access the world material in the same menu and change strength to 0.
11. Click on the 3D Viewport and press Shift+F11 to switch back to text editor.
12. Now 'open' up script 3. Choose whether you want instance segmentation or layerwise.
13. Run script 3. Monitor progress with the System Console.
14. Once all three scripts are run, check your directory for all output files.
15. Close the Blender window WITHOUT saving.
16. Now open a python environment in the repository directory and run script four.
17. Nothing should have to be changed manually and a folder called data should contain your split.
18. Now open up the normalisingTemplate.yaml. You can edit this directly and run or create a copy with a different name for specific setting.
19. Finally, run script 5 given direction below. End of data creation.

Run script 5 as follows:

    python script5_normalising_functions.py normalisingTemplate.yml
    
or

    python script5_normalising_functions.py <path to .yml file>

![A rendered training image](https://github.com/chowravc/OASIS_Segmentation_Training_Data_Generation/blob/main/ReadMeFiles/0.png?raw=true)

Fig 1. Example rendered train image

![A instance segmented mask](https://github.com/chowravc/OASIS_Segmentation_Training_Data_Generation/blob/main/ReadMeFiles/Cap58.png?raw=true)

Fig 2. Example instance segmented mask

![A non-instance segmented mask](https://github.com/chowravc/OASIS_Segmentation_Training_Data_Generation/blob/main/ReadMeFiles/1.png?raw=true)

Fig 3. Example non instance segmented mask

![A non-instance normalized image](https://github.com/chowravc/OASIS_Segmentation_Training_Data_Generation/blob/main/ReadMeFiles/04.png?raw=true)

Fig 3. Example normalized image
