#include <KLocalizedString>
#include <cassert>

int main()
{
    assert(ki18n("abcdef") == "abcdef");
    return 0;
}
