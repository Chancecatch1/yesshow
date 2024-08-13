<!-- frontend/src/routes/+page.svelte -->

<div class="w-full max-w-[950px] mx-auto p-4 -mb-16">
	<div class="w-full">
		<br />
		<br />
		<div
			class="text-black text-[8vw] md:text-[52px] font-extrabold font-['Nanum Gothic', 'Noto Sans KR', sans-serif] leading-tight"
		>
			당일 현장 <br /> 예매 취소표<br />
			<span class="text-[#696969]"> 예측 </span><br />
			서비스
		</div>

		<!-- 화살표 이미지 frontend/static/images/arrow-down.svg-->
		<div class="flex justify-center my-4">
			<div
				class="w-12 h-12 bg-[#696969] rounded-full flex items-center justify-center transform -translate-y-[140px] translate-x-[10px]"
			>
				<img src="/images/arrow-down.svg" alt="Arrow" class="w-6 h-6" />
			</div>
		</div>

		<!-- 박스 추가 -->
		<div
			class="flex justify-center my-4 top-[50%] transform -translate-y-[208px] translate-x-[300px]"
		>
			<a
				href="/service"
				class="inline-block w-[150px] h-[50px] bg-[#696969] rounded-[50px] flex items-center justify-center text-white text-lg font-semibold"
			>
				Service
			</a>
		</div>
	</div>
</div>
