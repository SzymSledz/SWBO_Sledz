addEventListener("DOMContentLoaded", (event) => {
    const navigationRoot = document.querySelector('img.nav-bar-menu');
    const navigationContent = document.querySelector('.navbar > .nav-level-1');
    if(navigationContent && navigationRoot)
    navigationRoot.addEventListener('click', () => {
        navigationContent.classList.toggle('hidden');
    })

    const navLevel2 = document.querySelectorAll('.nav-level-2.nav-root .inner-nav-expand');

    if(navLevel2){
        navLevel2.forEach(navExpand => {
            navExpand.addEventListener('click', (event) => {
                event.target.classList.toggle('is-active');
                const navigationRoot = event.target.parentElement.parentElement;
                const navLevel3 = navigationRoot.querySelectorAll('.nav-level-3');
                navLevel3.forEach(navElement => {
                    navElement.classList.toggle('hidden')
                })
            })
        })
    }


    const navLevel3Trigger = document.querySelectorAll('.inner-nav-expand');

});
