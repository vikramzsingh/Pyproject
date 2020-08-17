function A(f)
{
	if(require(f.T1,"Enter Your Name")==false)
	{
		f.T1.focus();
		return false;
		}
		
	else if(onlyalpha(f.T1,"Only Alphabets allowed")==false)
	{
		f.T1.value=null;//it empty the coloum
		f.T1.focus();
		return false;
		}
		
	else if(require(f.T2,"Enter Your Roll No.")==false)
	{
		f.T2.focus();
		return false;
		}
		
	else if(require(f.T3,"Enter Your Branch")==false)
	{
		f.T3.focus();
		return false;
		}
	
	else if(onlyalpha(f.T3,"Only Alphabets allowed")==false)
	{
		f.T3.value=null;//it empty the coloum
		f.T3.focus();
		return false;
		}
	else if(require(f.T4,"Enter Your Year")==false)
	{
		f.T4.focus();
		return false;
		}
		
	else if(require(f.T5,"Enter Your Address")==false)
	{
		f.T5.focus();
		return false;
		}
		
	else if(require(f.T6,"Enter Your Mobile No.")==false)
	{
		f.T6.focus();
		return false;
		}
	
	else if(onlydigit(f.T6,"Only digits allowed")==false)
	{
		f.T6.value=null;//it empty the coloum
		f.T6.focus();
		return false;
		}
	else if(digitrange(6000000000,9999999999,f.T6,"Enter valid number in range")==false)
	{
		f.T6.value=null;
		f.T6.focus();
		return false;
	}
		
	else if(require(f.T7,"Enter Your Email")==false)
	{
		f.T7.focus();
		return false;
		}
	else if(require(f.T8,"Enter Your Password")==false)
	{
		f.T8.focus();
		return false;
		}
	else if(require(f.T9,"Enter Your Confirm Password")==false)
	{
		f.T9.focus();
		return false;
		}
		
	else if(checkpass(f.T8,f.T9,"Confirm Password not matched")==false)
	{
		f.T9.value=null;
		f.T9.focus();
		return false;
		}
	}
	
function require(ele,msg)
{
	if(ele.value==null||ele.value=="")
	{
		alert(msg);
		return false;
		}	
	else
	{
		return true;
		}
	}
	
function onlyalpha(ele,msg)
{
	var letter=/^[a-z A-Z]+$/;
	if(ele.value.match(letter))
	{
		return true;
		}
	else
	{
		alert(msg);
		return false;
		}
	}

function onlydigit(ele,msg)
{
	var digit=/^[0-9]+$/;
	if(ele.value.match(digit))
	{
		return true;
		}
	else
	{
		alert(msg);
		return false;
		}
	}

function digitrange(mn,mx,ele,msg)
{
	if(ele.value<mn||ele.value>mx)
	{
		alert(msg);
		return false;	}
	else
	{
		return true;
	}
}

function checkpass(ele1,ele2,msg)
{
	if(ele1.value==ele2.value)
	{
		return true;
		}
	else
	{
		alert(msg);
		return false;
		}
	}
