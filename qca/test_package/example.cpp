#include <QtCrypto>
#include <QtPlugin>

Q_IMPORT_PLUGIN(opensslPlugin)

int main()
{
    return QCA::isSupported("md5");
}
