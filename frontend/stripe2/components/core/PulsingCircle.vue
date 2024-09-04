<template>
  <div class="pulse-base pulse-circle"></div>
</template>

<script>
export default {

}
</script>

<style scoped>
@keyframes pulsate {
  0% {
    transform: scale(0.6, 0.6);
    opacity: 0;
  }

  50% {
    opacity: 1;
  }

  100% {
    transform: scale(1, 1);
    opacity: 0;
  }
}
 .pulse-base {
   position: relative;
   height: 30px;
   width: 30px;
   border: 5px solid #222;
   border-radius: 50%;
   margin: 0 auto;
 }

 .pulse-circle {
   background: #86cfda;
 }

 .pulse-base:before {
   content: '';
   border: 15px solid rgba(255, 255, 255, 0.3);
   border-radius: 50%;
   height: 60px;
   width: 60px;
   position: absolute;
   left: -15px;
   bottom: -15px;
   animation: pulsate 1.6s ease-out;
   animation-iteration-count: infinite;
   opacity: 0;
   z-index: 99;
 }

</style>

