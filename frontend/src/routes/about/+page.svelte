<!-- frontend/src/routes/about/+page.svelte -->

<div class="w-full max-w-[1100px] h-auto relative mx-auto p-4 flex flex-col md:flex-row">
	<div class="md:w-2/3 w-full">
		<div class="text-2xl font-semibold mb-2">
			안녕하세요. 우리는
			<span class="text-[#696969]"> 북쏘 </span>
			<span class="text-2xl font-semibold mb-2"> 입니다. </span>
		</div>
		<span class="text-[#696969]"> YESSHOW는 특정 공연에 대해서 얼마나 그리고 언제</span>
		<span class="text-[#696969]"> 취소가 발생할지 예측합니다.</span> <br /><br />
		<span class="text-[#696969]">
			공연의 주최측은 선제적으로 취소에 대처하고, 대기 관객들에게 언제 취소가 발생할지 가능성을
			제안함으로써 보다 효과적으로 좌석을 운영할 수 있습니다. 더불어 추후 공연 설계시 도움이 될 수
			있도록 Kopis 빅데이터(2019년 7월 1일 ~ 2023년 12월 31일) 취소 분석을 통한 인사이트를
			제공합니다.</span
		> <br /><br />
		<span class="text-m">
			상단 메뉴에서
			<a href="/insight">Insight</a>
			클릭</span
		>
	</div>
</div>

<div class="w-full max-w-[1100px] h-auto relative mx-auto p-4 flex flex-col md:flex-row">
	<div class="md:w-2/3 w-full">
		<div class="text-2xl font-semibold mb-2">활용방법</div>
		<span class="text-[#696969]">
			상단의 Service 메뉴에서 공연코드를 선택합니다.(현재는 3개만 가능)</span
		> <br />
		<span class="text-[#696969]">
			선택한 공연에 대해서 해당되는 정보를 모두 입력하면 됩니다. 할인금액과 장당금액 그리고 연령은
			평균 값을 입력합니다. 성별의 경우 원본 데이터셋에서 0, 1, 2로 구별되어 있으며, 거기에 맞추어
			인원수를 입력하고 예측하기를 누르면 취소표의와 남은 좌석수를 예측할 수 있습니다. 남은 좌석수의
			경우는 좌석수에서 판매좌석수를 뺀 수치인데, 취소표 수 예측보다는 상대적으로 정확성이 떨어지니
			참고로 활용하시면 됩니다.
		</span> <br /><br />
		<span class="text-m">
			더불어 예측하기를 누르면 아래 쪽으로 취소표가 언제 발생할지 예측하는 인터랙티브 그래프를
			확인할 수 있습니다. 이를 참고해서 언제 취소 전략(예를 들면 추가 광고)를 수행할 지 예측할 수
			있습니다.</span
		>
	</div>
</div>

<div
	class="w-full max-w-[1100px] h-auto relative mx-auto p-4 flex flex-col md:flex-row justify-start gap-12 mt-8"
>
	<div
		class="w-full md:w-[21%] h-[100px] bg-[#fbfafc] rounded-[20px] border border-black flex justify-center items-center mb-4 md:mb-0"
	>
		<img src="/images/kams_logo.png" alt="KAMS Logo" class="w-[80%] h-auto" />
	</div>

	<div
		class="w-full md:w-[21%] h-[100px] bg-[#fbfafc] rounded-[20px] border border-black flex justify-center items-center mb-4 md:mb-0"
	>
		<img src="/images/kopis_logo.jpg" alt="KOPIS Logo" class="w-[80%] h-auto" />
	</div>
</div>
