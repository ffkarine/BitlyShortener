# Bitly Shortener

This script uses the Bitly API to shorten up to 1000 URLs (monthly limit defined by Bitly) <br>
It expects a csv file containing a column of IDs and a column of URLs to be shortened. <br>
It returns the shortened URLs on the same file, by adding a third column with them. <br>
<br>
To use this script you must have an account on Bitly and you must generate an OAUTH access token, which will be used to perform the shortening of the URLs.
After this, just edit the variables "path" to your csv file path, and pass your access token to the call of the method authentication(" -> YourAccessTokenHere <-")
