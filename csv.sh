#! /bin/sh -e

#EXAMPLE: sh csv.sh 20150615 20160615
#                   START    END
mongo calculus --eval "db.dropDatabase()"

#date -d '1 year ago' '+%Y%m%d'
#date -d '1 day ago' '+%Y%m%d'

start=$(date -d '1 year ago' '+%Y%m%d')
end=$(date -d '1 day ago' '+%Y%m%d')

python /var/www/html/fierybuild/data_controller.py --region Fremont --start $start --end  $end
python /var/www/html/fierybuild/data_controller.py --region IDC --start $start --end  $end
python /var/www/html/fierybuild/data_controller.py --region vCommander+Fremont --start $start --end  $end
python /var/www/html/fierybuild/data_controller.py --region vCommander+IDC --start $start --end  $end

python /var/www/html/fierybuild/linux_install_overhead_median.py
python /var/www/html/fierybuild/linux_install_overhead_mean.py
python /var/www/html/fierybuild/linux_install_duration_median.py
python /var/www/html/fierybuild/linux_install_duration_mean.py

python /var/www/html/fierybuild/windows_install_overhead_median.py
python /var/www/html/fierybuild/windows_install_overhead_mean.py
python /var/www/html/fierybuild/windows_install_duration_median.py
python /var/www/html/fierybuild/windows_install_duration_mean.py

python /var/www/html/fierybuild/linux_build_overhead_median.py
python /var/www/html/fierybuild/linux_build_overhead_mean.py
python /var/www/html/fierybuild/linux_build_duration_median.py
python /var/www/html/fierybuild/linux_build_duration_mean.py

python /var/www/html/fierybuild/windows_build_overhead_median.py
python /var/www/html/fierybuild/windows_build_overhead_mean.py
python /var/www/html/fierybuild/windows_build_duration_median.py
python /var/www/html/fierybuild/windows_build_duration_mean.py

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

