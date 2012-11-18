/**
 *  EverQuest S3D Extract
 */

#include <iostream>
#include <string>
#include <vector>

#include <s3d/boost_foreach.hpp>

#include <s3d/file.hpp>

bool bListFilenames           = false;
bool bExtractAllFiles         = true;
bool bExtractTextureFilesOnly = false;
bool bExtractWorldFilesOnly   = false;
bool bExtractSpecificFile     = false;

std::string sExtractSpecificFile;

int main(int argc, char *argv[])
{
    std::cout << "EverQuest S3D Extract" << std::endl;

    if (argc < 2)
    {
        std::cout << "Usage: s3d_extract.exe file.s3d (option)" << std::endl;
        std::cout << "Options:"                                          << std::endl;
        std::cout << "    -l             List Filenames, Do Not Extract" << std::endl;
        std::cout << "    -a             Extract All Files"              << std::endl;
        std::cout << "    -t             Extract Texture Files Only"     << std::endl;
        std::cout << "    -w             Extract World Files Only"       << std::endl;
        std::cout << "    -f filename    Extract Specific File"          << std::endl;
        std::cout << "Note: If option is omitted, Extract All Files is the default action." << std::endl;

        return 0;
    }

    if (argc > 2)
    {
        std::string option = argv[2];

        if (option == "-l" || option == "-list")
        {
            std::cout << "Option: List Filenames, Do No Extract" << std::endl;

            bListFilenames           = true;
            bExtractAllFiles         = false;
            bExtractTextureFilesOnly = false;
            bExtractWorldFilesOnly   = false;
            bExtractSpecificFile     = false;
        }

        if (option == "-a" || option == "-all")
        {
            std::cout << "Option: Extract All Files" << std::endl;

            bListFilenames           = false;
            bExtractAllFiles         = true;
            bExtractTextureFilesOnly = false;
            bExtractWorldFilesOnly   = false;
            bExtractSpecificFile     = false;
        }

        if (option == "-f" || option == "-file")
        {
            if (argc > 3)
            {
                std::cout << "Option: Extract Specific File" << std::endl;

                bListFilenames           = false;
                bExtractAllFiles         = false;
                bExtractTextureFilesOnly = false;
                bExtractWorldFilesOnly   = false;
                bExtractSpecificFile     = true;

                sExtractSpecificFile = argv[3];
            }
        }

        if (option == "-t" || option == "-textures")
        {
            std::cout << "Option: Extract Texture Files Only" << std::endl;

            bListFilenames           = false;
            bExtractAllFiles         = false;
            bExtractTextureFilesOnly = true;
            bExtractWorldFilesOnly   = false;
            bExtractSpecificFile     = false;
        }

        if (option == "-w" || option == "-world")
        {
            std::cout << "Option: Extract World Files Only" << std::endl;

            bListFilenames           = false;
            bExtractAllFiles         = false;
            bExtractTextureFilesOnly = false;
            bExtractWorldFilesOnly   = true;
            bExtractSpecificFile     = false;
        }
    }

    s3d::file file;
    file.open(argv[1]);

    std::cout << "File: "            << argv[1] << std::endl;
    std::cout << "Number Of Files: " << file.get_num_files() << std::endl;

    foreach (std::string filename, file.get_file_names())
        std::cout << "Filename: " << filename << std::endl;
    
    if (!bListFilenames)
    {
        if (bExtractAllFiles)
        {
            file.extract();
        }
        else
        {
            if (bExtractSpecificFile)
            {
                file.extract(true, true, true, sExtractSpecificFile);
            }
            else
            {
                file.extract(true, bExtractTextureFilesOnly, bExtractWorldFilesOnly);
            }
        }
    }

    file.close();

    return 0;
}
