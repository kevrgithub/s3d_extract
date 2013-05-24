g++ --version
g++ s3d_extract.cpp -Id:\code\s3d\include -Ld:\code\s3d\lib -Id:\code\_libraries\boost\include -Ld:\code\_libraries\boost\lib -Id:\code\_libraries\zlib\include -Ld:\code\_libraries\zlib\lib -lboost_system -lboost_iostreams -lboost_filesystem -lz -Wl,--enable-auto-import -Wl,-subsystem,console -Wall -O0 -s -o release/s3d_extract.exe
pause
