<!-- frontend/src/routes/+page.svelte -->

<div
	class="w-full max-w-[90%] md:max-w-[70%] lg:max-w-[60%] xl:max-w-[50%] mx-auto flex flex-col justify-center items-center p-4 md:p-8 lg:p-10 mt-8 md:mt-16 lg:mt-20"
>
	<div
		class="text-center text-black text-xl sm:text-2xl md:text-3xl lg:text-4xl font-extrabold font-['Nanum Gothic', 'Noto Sans KR', sans-serif] leading-tight mb-4"
	>
		<div class="mb-1 sm:mb-2 leading-normal sm:leading-snug">당일 현장</div>
		<div class="mb-1 sm:mb-2 leading-normal sm:leading-snug">예매 취소표</div>
		<div class="text-[#696969] mb-1 sm:mb-2 leading-normal sm:leading-snug">예측</div>
		<div class="leading-normal sm:leading-snug">서비스</div>
	</div>

	<!-- 박스를 글자 아래로 이동 -->
	<div class="mt-6">
		<a
			href="/service"
			class="inline-block w-[100px] h-[35px] sm:w-[120px] sm:h-[40px] md:w-[130px] md:h-[45px] bg-[#696969] rounded-[50px] flex items-center justify-center text-white text-sm sm:text-base md:text-lg font-semibold"
		>
			GO
		</a>
	</div>
</div>
