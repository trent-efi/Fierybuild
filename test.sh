#! /bin/sh -e

python /var/www/html/fierybuild/weekly_linux_build_duration_mean.py
python /var/www/html/fierybuild/weekly_linux_build_overhead_mean.py
python /var/www/html/fierybuild/weekly_linux_build_duration_median.py
python /var/www/html/fierybuild/weekly_linux_build_overhead_median.py

python /var/www/html/fierybuild/weekly_linux_install_duration_mean.py
python /var/www/html/fierybuild/weekly_linux_install_overhead_mean.py
python /var/www/html/fierybuild/weekly_linux_install_duration_median.py
python /var/www/html/fierybuild/weekly_linux_install_overhead_median.py

python /var/www/html/fierybuild/weekly_windows_build_duration_mean.py
python /var/www/html/fierybuild/weekly_windows_build_overhead_mean.py
python /var/www/html/fierybuild/weekly_windows_build_duration_median.py
python /var/www/html/fierybuild/weekly_windows_build_overhead_median.py

python /var/www/html/fierybuild/weekly_windows_install_duration_mean.py
python /var/www/html/fierybuild/weekly_windows_install_overhead_mean.py
python /var/www/html/fierybuild/weekly_windows_install_duration_median.py
python /var/www/html/fierybuild/weekly_windows_install_overhead_median.py

