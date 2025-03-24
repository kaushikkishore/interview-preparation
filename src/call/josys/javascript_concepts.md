
```
for (let i=0; i<10; i++) {
        const time = Math.floor(Math.random() * 101);
        const res = setTimeout(() => {
            console.log('i::::::::::::', i);
        }, time);
    }
```

- Print what will be the result of the above code. 
- Then make sure you print the code in the 0..9 order. Which is how do you will convert the setTimeout function as promise or use as async await. 



```
async function printSequence() {
    for (let i = 0; i < 10; i++) {
        await new Promise(resolve => {
            const time = Math.floor(Math.random() * 101);
            setTimeout(() => {
                console.log('i:', i);
                resolve();
            }, time);
        });
    }
}

printSequence();

```