#include <QCoreApplication>
#include"scan.h"
int main(int argc, char *argv[])
{

   std::string  path = "/home/zhangjian/Downloads/ScannerLite-master 2/Scanner/images/doc3.jpg";
   Mat image = scan(path);
   imshow("img",image);
    QCoreApplication a(argc, argv);

    return a.exec();
}
