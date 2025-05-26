Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
Some packages could not be installed. This may mean that you have
requested an impossible situation or if you are using the unstable
distribution that some required packages have not yet been created
or been moved out of Incoming.
The following information may help to resolve the situation:

The following packages have unmet dependencies:
 mono-complete : Depends: mono-runtime (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-runtime-sgen (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-utils (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-devel (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-mcs (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-csharp-shell (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-4.0-gac (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: mono-4.0-service (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: monodoc-base (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: monodoc-manual (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: libmono-cil-dev (= 6.8.0.105+dfsg-3.3) but it is not going to be installed
                 Depends: ca-certificates-mono (= 6.8.0.105+dfsg-3.3) but it is not going to be installed

sudo apt install gnupg ca-certificates -y
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
