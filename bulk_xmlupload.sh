#reqire lot of customization
for i in {0..65..1}
do
    if [ -f ./kk310/$i/build.xml ]; then
        echo "Taking care of build $i"
        python upload_buildxml.py ./kk310/$i/build.xml kk310_android $i
        sleep 1
    fi
done
