#include <QtCrypto>
#include <QtPlugin>

#ifndef QCA_SHARED
Q_IMPORT_PLUGIN(opensslPlugin)
#endif

int main()
{
    return QCA::isSupported("md5");
}
