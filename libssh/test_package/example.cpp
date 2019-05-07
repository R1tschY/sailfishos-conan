#include <cstdio>
#include <cstring>
#include <libssh/libssh.h>

int main()
{
    int ret = ssh_init();
    if (ret != 0)
        return 1;

    char* result = ssh_get_hexa(
        reinterpret_cast<const unsigned char*>("\x01\x02\x03"), 3);
    if (strcmp(result, "01:02:03") != 0) {
        return 2;
    }
    ssh_string_free_char(result);

    ret = ssh_finalize();
    if (ret != 0)
        return 3;

    return 0;
}
