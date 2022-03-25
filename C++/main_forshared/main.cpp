#include <iostream>
#include <time.h>
#include <windows.h>

typedef void (*MYPROC)(int *list, int, int);

void print(int *list, int n)
{
    for(int i = 0; i < n; i++)
    {
        printf("%4d", list[i]);
    }
    puts("");
}

int main()
{
    int n;
    std::cout << "Enter the length of your array:\n";
    std::cin >> n;
    int *list = new int[n];
    srand(time(nullptr));
    for(int i = 0; i < n; i++)
    {
        list[i] = rand() % 199 - 99;
    }
    std::cout << "Your original array:" << std::endl;
    print(list, n);
    MYPROC merge_sort;
    HINSTANCE hinstLib = LoadLibrary(TEXT("libmerge_shared_lib.dll"));
    merge_sort = (MYPROC) GetProcAddress(hinstLib, TEXT("merge_sort"));
    if (hinstLib != nullptr)
    {
        if(merge_sort != nullptr)
        {
            std::cout << "Your sorted array:" << std::endl;
            merge_sort(list, 0, n - 1);
            print(list, n);
        } else
        {
            DWORD dwError = GetLastError();
            std:: cout << "Function hasn`t been found" << std::endl;
        }
        FreeLibrary(hinstLib);
    } else
    {
        std::cout << "Library hasn`t been found " << std::endl;
    }
    delete [] list;
    return 0;
}

