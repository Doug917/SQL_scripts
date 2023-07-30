/*saved query to use in SSMS*
updates table primes (p int) with prime numbers up to inputted value N*/
/*When first using, you need to create the primes table and use the following code,
replacing 'alter procedure' with 'create procedure'*/

alter procedure add_primes @N int
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
