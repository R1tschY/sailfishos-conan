#include <KConfig>
#include <cassert>

int main()
{
    KConfig::setMainConfigName("config.config");
    return 0;
}
