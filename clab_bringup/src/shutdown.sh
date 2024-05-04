

sync; echo 1 > /proc/sys/vm/drop_caches  #FOR CLEARING CACHES FROM RAM


sync; echo 2 > /proc/sys/vm/drop_caches  #FOR CLEARING CACHES FROM RAM


sync; echo 3 > /proc/sys/vm/drop_caches  #FOR CLEARING CACHES FROM RAM


shutdown


sudo systemctl stop start_ros.service    #STOPPING ALL THE PROCESS