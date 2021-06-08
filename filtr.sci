function t=biquad(h)

// (c) 2007 Robert Wirski (r.wirski@ieee.org)

[l,m,g]=factors(h);
lenl=length(l);
for i=lenl:-1:1
  if polyord(l(i))==1
    for j=1:i-1
      if polyord(l(j))==1
        l(j) = l(j) * l(i);
        l(i) = null();
        break;
      end;
    end;
  end;
end;
lenm=length(m);
for i=lenm:-1:1
  if polyord(m(i))==1
    for j=1:i-1
      if polyord(m(j))==1
        m(j) = m(j) * m(i);
        m(i) = null();
        break;
      end;
    end;
  end;
end;
len = length(l);
if modulo(len,2)
  l($+1)=%z^2;
  m($+1)=%z^2;
  len=len+1;
end;
if len~=length(m)
  error('Internal error');
end;
printf('TotalAmp: %.3f\nnumSections: %i\n',g,len);
printf('coeffs:\nIdx\tVal\n');
for i=1:2:len-1
  mc1=coeff(m(i));
  mc2=coeff(m(i+1));
  lc1=coeff(l(i));
  lc2=coeff(l(i+1));
  printf('%i\t%.5f\n',((0:7)+(i-1)*4)',[-mc1(1);-mc2(1);-mc1(2);-mc2(2);lc1(1);lc2(1);lc1(2);lc2(2)]);
end;
t=list(g);
for i=1:len
  t($+1)=l(i)/m(i);
end;
endfunction   
  
function r=polyord(p)
  r = length(coeff(p))-1;
endfunction
h=iir(6,'lp','butt',[4200 8800]/44100,[1-10^(-1.8/20) 10^(-32/20)]);
hk=biquad(h);

hk1 = hk(1)*hk(2);
hk2 = hk(3);
hk3 = hk(4);

toJSON(coeff([hk1.num;hk1.den]), "hk1.json");
toJSON(coeff([hk2.num;hk2.den]), "hk2.json");
toJSON(coeff([hk3.num;hk3.den]), "hk3.json");


