$(document).ready(function(){
$('.slider').bxSlider();
});

const partners = document.querySelectorAll('.partners .img')
window.addEventListener("scroll",()=>{
    if(window.innerWidth < 700){        
        if(window.scrollY > 0){
            document.querySelector(".menubar").classList.add("scroll");
            document.querySelector(".findjob h1").classList.add("scroll")
        }
        else{
            document.querySelector(".menubar").classList.remove("scroll")
        }
        
        if(window.scrollY > window.innerHeight * 0.5){
            document.querySelector(".whatwedo img").classList.add("scroll")
            if (document.querySelector(".menuitems2").classList.contains("click")){
                document.querySelector(".menuitems2").classList.remove("click")
            }
        }
    
        if(window.scrollY > window.innerHeight * 2.25){
            document.querySelector(".webuild .textarea h1").classList.add("scroll")            
        }
    
        if(window.scrollY > window.innerHeight * 3.5){
            document.querySelector(".webuild .createacc").classList.add("scroll") 
            document.querySelector(".webuild img").classList.add("scroll")       
        }
    
        if(window.scrollY > window.innerHeight * 4){
            document.querySelector(".hotlisting img").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 5){
            document.querySelector(".hotlisting .buttons").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 5.5){
            document.querySelector(".success h2").classList.add("scroll")        
        }
        var x = 0;
        if(window.scrollY > window.innerHeight * 6){
            document.querySelectorAll(".trending .card").forEach((slidleft)=>{
                if(window.scrollY > window.innerHeight * 6 + x){
                    slidleft.classList.add("scroll")
                    x+=450;
                }
            })       
        }      
        
    }
    else{
        if(window.scrollY > 0){
            document.querySelector(".menubar").classList.add("scroll");
            document.querySelector(".findjob h1").classList.add("scroll")
        }
        else{
            document.querySelector(".menubar").classList.remove("scroll")
        }
        
        if(window.scrollY > window.innerHeight * 1){
            document.querySelector(".whatwedo img").classList.add("scroll")
        }
    
        if(window.scrollY > window.innerHeight * 1.9){
            document.querySelector(".webuild .textarea h1").classList.add("scroll")
            document.querySelector(".webuild img").classList.add("scroll")
        }
    
        if(window.scrollY > window.innerHeight * 2.5){
            document.querySelector(".webuild .createacc").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 3.5){
            document.querySelector(".hotlisting img").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 3.7){
            document.querySelector(".hotlisting .buttons").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 4.5){
            document.querySelector(".success h2").classList.add("scroll")        
        }
    
        if(window.scrollY > window.innerHeight * 5){
            document.querySelectorAll(".trending .card").forEach((slidleft)=>{
                slidleft.classList.add("scroll")
            })
        }
    }
})

function clicked(){
    document.querySelector(".menuitems2").classList.toggle("click") 
}