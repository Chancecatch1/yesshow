<!-- frontend/src/routes/about/+page.svelte -->

<div class="container mx-auto p-4 flex flex-col md:flex-row max-w-4xl">
	<div class="md:w-2/3 w-full">
		<h2 class="text-2xl font-semibold mb-2">
			안녕하세요 <span class="text-gray-500">북쏘</span> 입니다
		</h2>
		<p class="text-gray-500 mb-4">
			"예스쇼 - Yesshow" 는 특정 공연에 대해서 얼마나 그리고 언제 취소가 발생할지 예측하는
			서비스입니다. 이를 통해 공연 주최측은 선제적으로 취소에 대처하며 대기 관객들에게 언제 취소가
			발생할지 가능성을 제안합니다. <br />
			더불어 Kopis 빅데이터(19.7.1. ~ 23. 12. 31.) 분석에 따른 공연 취소 요인을 제공합니다. <br />
			상단 메뉴에서
			<a href="/insight" class="font-bold underline hover:text-blue-600">Insight</a> 클릭
		</p>
	</div>
</div>

<div class="container mx-auto p-4 flex flex-col md:flex-row max-w-4xl mt-2">
	<div class="md:w-2/3 w-full">
		<h2 class="text-2xl font-semibold mb-2">
			취소 <span class="text-gray-500">예측 서비스</span> 활용방법
		</h2>
		<p class="text-gray-500 mb-4">
			상단의 Service 메뉴에서 공연코드를 선택합니다.(현재는 3개만 가능) <br /> 선택한 공연과
			공연일시 대해서 해당되는 정보를 모두 입력합니다. 할인금액과 장당금액 그리고 연령은 평균 값을
			입력하며, 성별의 경우는 0, 1, 2로 구별되며, 각 인원수를 입력합니다.(원본 데이터셋의 분류에
			따름) 결제구분과 할인종류 역시 해당하는 인원수를 입력합니다. 모든 정보를 입력하고 '예측하기'
			버튼을 누르면 취소수(예매 / 취소구분에서 취소의 합)와 남은 좌석수를 예측할 수 있습니다. 남은
			좌석수의 경우는 원본 데이터셋의 좌석수에서 판매좌석수를 뺀 합성 특성입니다.
			<br />
			더불어 예측하기를 누르면 하단으로 취소 발생 시점 인터랙티브 그래프를 확인할 수 있습니다. 이 그래프를
			통해 선제적 취소 전략(추가 광고 등)에 활용할 수 있습니다.
		</p>
	</div>
</div>

<div class="container mx-auto p-4 flex flex-col md:flex-row justify-start gap-6 max-w-4xl mt-2">
	<div
		class="w-full md:w-1/5 h-[100px] bg-white rounded-2xl border border-black flex justify-center items-center"
	>
		<img src="/images/kams_logo.png" alt="KAMS Logo" class="w-4/5 h-auto" />
	</div>

	<div
		class="w-full md:w-1/5 h-[100px] bg-white rounded-2xl border border-black flex justify-center items-center"
	>
		<img src="/images/kopis_logo.jpg" alt="KOPIS Logo" class="w-4/5 h-auto" />
	</div>
</div>
