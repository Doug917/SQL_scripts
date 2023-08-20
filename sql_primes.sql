/*saved query to use in SSMS*
updates table primes (p int) with prime numbers up to inputted value N*/
/*When first using, you need to create the primes table by running the following code.
To run the procedure to generate all primes less than 1000, run:
exec add_primes @N = 1000.*/

create procedure add_primes @N int
as
begin
	declare @i int
	declare @c int
	set @i =
	(select max(p)
	from primes)
	while (@i <= @N)
	begin
		set @c = 
		(select count(*)
		from
		(select p
		from primes
		where @i % p = 0) as tempTable)

		if @c = 0
			insert into primes (p) values (@i)

		set @i = @i + 1
	end
end


/*Example queries:
1.  print out the number of twin primes between 1 and 1000.

SELECT 2 * COUNT(P.q) as NumTwinPrimes
FROM primes P JOIN primes Q
on P.p = Q.p - 2

2.  list all the semiprimes that are less than 1,000,000.

select P.p, Q.p, P.p * Q.p as Semiprime
from primes P cross join primes Q
where P.p * Q.p < 1000000
and P.p < Q.p
order by P.p*Q.p ASC;

