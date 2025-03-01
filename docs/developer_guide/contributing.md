# Contributor Guidelines

## Make Tips
`ROCM_PATH` is path where ROCM is installed. BY default `ROCM_PATH` is `/opt/rocm`.
When building HIP, you will likely want to build and install to a local user-accessible directory (rather than `<ROCM_PATH>`).
This can be easily be done by setting the `-DCMAKE_INSTALL_PREFIX` variable when running cmake.  Typical use case is to
set `CMAKE_INSTALL_PREFIX` to your HIP git root, and then ensure `HIP_PATH` points to this directory. For example

```shell
cmake .. -DCMAKE_INSTALL_PREFIX=..
make install

export HIP_PATH=
```

After making HIP, don't forget the "make install" step !



## Adding a new HIP API
- Add a translation to the hipify-clang tool ; many examples abound.
    - For stat tracking purposes, place the API into an appropriate stat category ("dev", "mem", "stream", etc).
- Add a inlined NVIDIA implementation for the function in include/hip/nvidia_detail/hip_runtime_api.h.
    - These are typically headers
- Add an HIP_ROCclr definition and Doxygen comments for the function in include/amd_detail/hip_runtime_api.h
    - Source implementation typically go in hip/rocclr/hip_*.cpp. The implementation involve calls to HIP runtime (ie for hipStream_t).

## Check HIP-Clang version
In some cases new HIP-Clang features are tied to specified releases, and it can be useful to check the current version is sufficiently new enough to support the desired feature.

HIP runtime version

```console
> cat <ROCM_PATH>/hip/bin/.hipVersion
# Auto-generated by cmake
HIP_VERSION_MAJOR=3
HIP_VERSION_MINOR=9
HIP_VERSION_PATCH=20345-519ef3f2
```

HIP-Clang compiler version

```console
$ <ROCM_PATH>/llvm/bin/clang -v
clang version 11.0.0 (/src/external/llvm-project/clang 075fedd3fd2f4d9d8cca79d0cd51f64c5ef21432)
Target: x86_64-unknown-linux-gnu
Thread model: posix
InstalledDir: <ROCM_PATH>/llvm/bin
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/7.5.0
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/8
Found candidate GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Selected GCC installation: /usr/lib/gcc/x86_64-linux-gnu/9
Candidate multilib: .;@m64
Candidate multilib: 32;@m32
Candidate multilib: x32;@mx32
Selected multilib: .;@m64
```

## Unit Testing Environment

HIP includes unit tests in the tests/src directory.
When adding a new HIP feature, add a new unit test as well.
See [tests/README.md](README.md) for more information.

## Development Flow

Directed tests provide a great place to develop new features alongside the associated test.

For applications and benchmarks outside the directed test environment, developments should use a two-step development flow:
- #1. Compile, link, and install HIP/ROCclr.  See [Installation](README.md#Installation) notes.
- #2. Relink the target application to include changes in HIP runtime file.

## Environment Variables
- **HIP_PATH** : Location of HIP include, src, bin, lib directories.
- **HCC_ROCCLR_HOME** : Path to HIP/ROCclr directory, used on AMD platforms.  Default <ROCM_PATH>/rocclr.
- **HSA_PATH** : Path to HSA include, lib.  Default <ROCM_PATH>/hsa.
- **CUDA_PATH* : On nvcc system, this points to root of CUDA installation.

## Contribution guidelines ##

Features (ie functions, classes, types) defined in hip*.h should resemble CUDA APIs.
The HIP interface is designed to be very familiar for CUDA programmers.

Differences or limitations of HIP APIs as compared to CUDA APIs should be clearly documented and described.

### Coding Guidelines (in brief)
- Code Indentation:
    - Tabs should be expanded to spaces.
    - Use 4 spaces indentation.
- Capitalization and Naming
    - Prefer camelCase for HIP interfaces and internal symbols.  Note HCC uses _ for separator.
      This guideline is not yet consistently followed in HIP code - eventual compliance is aspirational.
    - Member variables should begin with a leading "_".  This allows them to be easily distinguished from other variables or functions.

- {} placement
    - For functions, the opening { should be placed on a new line.
    - For if/else blocks, the opening { is placed on same line as the if/else. Use a space to separate {/" from if/else.  Example
'''
    if (foo) {
        doFoo()
    } else {
        doFooElse();
    }
'''
    - namespace should be on same line as { and separated by a space.
    - Single-line if statement should still use {/} pair (even though C++ does not require).
- Miscellaneous
    - All references in function parameter lists should be const.
    - "ihip" = internal hip structures.  These should not be exposed through the HIP API.
    - Keyword TODO refers to a note that should be addressed in long-term.  Could be style issue, software architecture, or known bugs.
    - FIXME refers to a short-term bug that needs to be addressed.

- HIP_INIT_API() should be placed at the start of each top-level HIP API.  This function will make sure the HIP runtime is initialized,
  and also constructs an appropriate API string for tracing and CodeXL marker tracing.  The arguments to HIP_INIT_API should match
  those of the parent function.
- ihipLogStatus should only be called from top-level HIP APIs,and should be called to log and return the error code.  The error code
  is used by the GetLastError and PeekLastError functions - if a HIP API simply returns, then the error will not be logged correctly.

- All HIP environment variables should begin with the keyword HIP_
    Environment variables should be long enough to describe their purpose but short enough so they can be remembered - perhaps 10-20 characters, with 3-4 parts separated by underscores.
    To see the list of current environment variables, along with their values, set HIP_PRINT_ENV and run any hip applications on ROCm platform .
    HIPCC or other tools may support additional environment variables which should follow the above convention.


### Presubmit Testing:
Before checking in or submitting a pull request, run all directed tests (see tests/README.md) and all Rodinia tests.
Ensure pass results match starting point:

```console
> cd examples/
> ./run_all.sh
```


### Checkin messages
Follow existing best practice for writing a good Git commit message.    Some tips:
    http://chris.beams.io/posts/git-commit/
    https://robots.thoughtbot.com/5-useful-tips-for-a-better-commit-message

In particular :
   - Use imperative voice, ie "Fix this bug", "Refactor the XYZ routine", "Update the doc".
     Not : "Fixing the bug", "Fixed the bug", "Bug fix", etc.
   - Subject should summarize the commit.  Do not end subject with a period.  Use a blank line
     after the subject.



## Doxygen Editing Guidelines

- bugs should be marked with @bugs near the code where the bug might be fixed.  The @bug message will appear in the API description and also in the
doxygen bug list.

##  Other Tips:
### Markdown Editing
Recommended to use an offline Markdown viewer to review documentation, such as Markdown Preview Plus extension in Chrome browser, or Remarkable.
