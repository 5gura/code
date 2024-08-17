#!/bin/bash

encrypt_files_path="/home/user/"
decrypt_files_path="/home/user/test_dhu/decrypt/"
zi_files="test_dhu"
log_file="/home/user/log.txt"

pre_files_path(){
    cd $encrypt_files_path
    if  test -e $zi_files 
    then
        echo '加密文件夹已存在!'
    else
        echo '加密文件夹不存在!'
    fi
}
pre_file_path(){
    test -e $zi_files && cd $zi_files
    if ls . | grep [0-9][0-9]
    then 
        echo '加密文件已存在!'
    else
        echo '加密文件不存在!'
    fi
}

decrypt(){
    #find . -type f  -exec openssl enc -d -aes-128-ctr -in {} -out ${decrypt_files_path}/{}'.mp4'  -k 'password' \;
    for file_path in ${encrypt_files_path}/${zi_files}/*; do
    if [ -f "$file_path" ]; then
    file_name=$(basename "$file_path")
    openssl enc -d -aes-128-ctr -in ${file_name} -out ${decrypt_files_path}/${file_name}'.mp4'  -k 'password'
    echo "File '${file_name}' decrypted successfully."
    ffmpeg -i ${decrypt_files_path}/${file_name}'.mp4' ${decrypt_files_path}/${file_name}'.mkv'
    aws s3 cp ${decrypt_files_path}/${file_name}'.mkv' s3://links/${file_name}'.mkv'  --region ap-northeast-1
    echo "File '${file_name}' uploaded successfully."
    rm ${decrypt_files_path}/${file_name}'.mp4'
    rm ${decrypt_files_path}/${file_name}'.mkv'
    echo "removed file '${file_name}'"
    fi
    done
}

pre_files_path
pre_file_path
decrypt > ${log_file}