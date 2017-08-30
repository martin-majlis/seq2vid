# Seq2Vid

Seq2Vid is tool for visualizing sequence of integers.

## Example

	# Input file where each line contains single number
	seq 1 10000 | sort -R | head -n 5000 | sort -n > inp.txt
	# Generate video
	python seq2vid.py --inp inp.txt --out out --min 1 --max 10000 --footer 'seq2vid' --header 'seq2vid - demo'


## Youtube
* Youtube requires 16:9 ratio.
* [Recommended resolution & aspect ratios](https://support.google.com/youtube/answer/6375112)
* [Recommended upload encoding settings](https://support.google.com/youtube/answer/1722171?hl=en)




## Generating Videos
### Export From DB
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'add' ORDER BY num;" > primes-add.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'chen' ORDER BY num;" > primes-chen.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'pco' ORDER BY num;" > primes-pco.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'emi' ORDER BY num;" > primes-emi.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'good' ORDER BY num;" > primes-good.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'hap' ORDER BY num;" > primes-hap.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'har' ORDER BY num;" > primes-har.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'iso' ORDER BY num;" > primes-iso.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'long' ORDER BY num;" > primes-long.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'luck' ORDER BY num;" > primes-luck.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'prime' ORDER BY num;" > primes-prime.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'p3' ORDER BY num;" > primes-p3.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'pyt' ORDER BY num;" > primes-pyt.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'safe' ORDER BY num;" > primes-safe.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'semi' ORDER BY num;" > primes-semi.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'pse2' ORDER BY num;" > primes-pse2.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'pse3' ORDER BY num;" > primes-pse3.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'sg' ORDER BY num;" > primes-sg.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'super' ORDER BY num;" > primes-super.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'p2' ORDER BY num;" > primes-p2.txt
	mysql -u $MYSQL_USER -p -B -N -D primenumbers -e "select num from indices WHERE k = 'ula' ORDER BY num;" > primes-ula.txt


### Seq2Vid commands
	python seq2vid.py --inp primes-add.txt --out video-add --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Additive primes: 1 - 1M' | tee log-add.log
	python seq2vid.py --inp primes-chen.txt --out video-chen --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Chen primes: 1 - 1M' | tee log-chen.log
	python seq2vid.py --inp primes-pco.txt --out video-pco --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Cousin primes: 1 - 1M' | tee log-pco.log
	python seq2vid.py --inp primes-emi.txt --out video-emi --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Emirps: 1 - 1M' | tee log-emi.log
	python seq2vid.py --inp primes-good.txt --out video-good --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Good primes: 1 - 1M' | tee log-good.log
	python seq2vid.py --inp primes-hap.txt --out video-hap --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Happy primes: 1 - 1M' | tee log-hap.log
	python seq2vid.py --inp primes-har.txt --out video-har --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Harmonic primes: 1 - 1M' | tee log-har.log
	python seq2vid.py --inp primes-iso.txt --out video-iso --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Isolated primes: 1 - 1M' | tee log-iso.log
	python seq2vid.py --inp primes-long.txt --out video-long --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Long primes: 1 - 1M' | tee log-long.log
	python seq2vid.py --inp primes-luck.txt --out video-luck --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Lucky primes: 1 - 1M' | tee log-luck.log

	python seq2vid.py --inp primes-prime.txt --out video-prime --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Prime numbers: 1 - 1M' | tee log-prime.log
	python seq2vid.py --inp primes-p3.txt --out video-p3 --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Prime triplets: 1 - 1M' | tee log-p3.log
	python seq2vid.py --inp primes-pyt.txt --out video-pyt --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Pythagorean primes: 1 - 1M' | tee log-pyt.log
	python seq2vid.py --inp primes-safe.txt --out video-safe --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Safe primes: 1 - 1M' | tee log-safe.log
	python seq2vid.py --inp primes-semi.txt --out video-semi --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Semiprimes: 1 - 1M' | tee log-semi.log
	python seq2vid.py --inp primes-pse2.txt --out video-pse2 --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Sexy primes: 1 - 1M' | tee log-pse2.log
	python seq2vid.py --inp primes-pse3.txt --out video-pse3 --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Sexy prime triplets: 1 - 1M' | tee log-pse3.log
	python seq2vid.py --inp primes-sg.txt --out video-sg --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Sophie Germain primes: 1 - 1M' | tee log-sg.log
	python seq2vid.py --inp primes-super.txt --out video-super --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Super primes: 1 - 1M' | tee log-super.log
	python seq2vid.py --inp primes-p2.txt --out video-p2 --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Twin primes: 1 - 1M' | tee log-p2.log
	python seq2vid.py --inp primes-ula.txt --out video-ula --min 1 --max 1048576 --footer 'prime-numbers.info' --header 'Ulam primes: 1 - 1M' | tee log-ula.log


### Install OpenCV on Ubuntu 16.04
	https://launchpad.net/~lkoppel/+archive/ubuntu/opencv
	sudo add-apt-repository ppa:lkoppel/opencv;
	sudo apt-get update;
	sudo apt-get install python-opencv;



