#! /bin/sh -e

#EXAMPLE: sh csv.sh 20150615 20160615
mongo calculus --eval "db.dropDatabase()"

python data_controller.py --region Fremont --start $1 --end  $2
python data_controller.py --region IDC --start $1 --end  $2
python data_controller.py --region vCommander+Fremont --start $1 --end  $2
python data_controller.py --region vCommander+IDC --start $1 --end  $2

python linux_install_overhead_median.py
python linux_install_overhead_mean.py
python linux_install_duration_median.py
python linux_install_duration_mean.py

python windows_install_overhead_median.py
python windows_install_overhead_mean.py
python windows_install_duration_median.py
python windows_install_duration_mean.py

python linux_build_overhead_median.py
python linux_build_overhead_mean.py
python linux_build_duration_median.py
python linux_build_duration_mean.py

python windows_build_overhead_median.py
python windows_build_overhead_mean.py
python windows_build_duration_median.py
python windows_build_duration_mean.py

python weekly_linux_build_duration_mean.py
python weekly_linux_build_overhead_mean.py
python weekly_linux_build_duration_median.py
python weekly_linux_build_overhead_median.py

python weekly_linux_install_duration_mean.py
python weekly_linux_install_overhead_mean.py
python weekly_linux_install_duration_median.py
python weekly_linux_install_overhead_median.py

python weekly_windows_build_duration_mean.py
python weekly_windows_build_overhead_mean.py
python weekly_windows_build_duration_median.py
python weekly_windows_build_overhead_median.py

python weekly_windows_install_duration_mean.py
python weekly_windows_install_overhead_mean.py
python weekly_windows_install_duration_median.py
python weekly_windows_install_overhead_median.py

