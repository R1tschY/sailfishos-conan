#include <QtCrypto>

int main()
{
    return QCA::isSupported("md5");
}
