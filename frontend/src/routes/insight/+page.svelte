<!-- frontend/src/routes/insight/+page.svelte -->

<script lang="ts">
	import { fade } from 'svelte/transition';
	let analysisType = '';

	function handleAnalysisTypeChange(event) {
		analysisType = event.target.value;
	}
</script>

<main class="w-full max-w-[850px] mx-auto p-4 relative">
	<div class="relative">
		<h1 class="text-2xl font-bold mb-4">
			공연 취소에 영향을 미치는
			<span class="text-[#696969]"> 요인 </span>
		</h1>

		<div class="mt-8">
			<h2 class="text-l font-semibold mb-2">분석 유형 선택</h2>
			<div class="flex items-center gap-4">
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<select
						id="analysisType"
						bind:value={analysisType}
						on:change={handleAnalysisTypeChange}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						style="font-family: 'Noto Sans KR', sans-serif;"
						required
					>
						<option value="" disabled selected>분석 유형 선택</option>
						<option value="genre">장르</option>
						<option value="facility">시설특성</option>
						<option value="location">공연지역</option>
						<option value="paymentMethod">결제수단</option>
						<option value="discountType">할인종류</option>
						<option value="childPerformance">아동공연 여부</option>
						<option value="performanceDate">공연일시</option>
						<option value="weather">날씨</option>
						<option value="gender">성별</option>
						<option value="age">연령</option>
						<option value="openingYear">개관연도</option>
						<option value="discountAmount">할인금액</option>
						<option value="ticketPrice">장당금액</option>
					</select>
				</div>
			</div>
		</div>
	</div>
	{#if analysisType === 'genre'}
		<div in:fade class="mt-4">
			<img
				src="/images/Genre_Counts_Cancellation_Rates.png"
				alt="Genre Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 해당 장르의 공연 수를 나타내며, 선그래프는 취소율의 추이를 나타냅니다.
				<br /><br />

				뮤지컬 장르가 공연수에서 가장 많았고, 대중무용의 경우 장르의 공연 숫자에 비해 취소율이
				상대적으로 높았습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 장르 목록</p>
				<ul class="list-disc list-inside space-y-1">
					<li>뮤지컬 (Musical)</li>
					<li>대중음악 (Pop Music)</li>
					<li>연극 (Play)</li>
					<li>서양음악(클래식) (Western Music (Classical))</li>
					<li>무용(서양/한국무용) (Dance (Western/Korean))</li>
					<li>한국음악(국악) (Korean Music (Traditional))</li>
					<li>서커스/마술 (Circus/Magic)</li>
					<li>복합 (Mixed)</li>
					<li>대중무용 (Pop Dance)</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'facility'}
		<div in:fade class="mt-4">
			<img
				src="/images/Facility_Counts_Cancellation_Rates.png"
				alt="Facility Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 시설유형별 공연수를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				민간(대학로 외) 시설이 가장 많은 공연수를 가지고 있고 취소율도 상대적으로 높았습니다. 반면,
				공공(문예회관)의 경우 공연수가 비교적 많은데 비해 취소율은 낮은 추이를 보이고 있습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 시설 유형 목록</p>
				<ul class="list-disc list-inside space-y-1">
					<li>민간(대학로 외) (Private (Outside Daehak-ro))</li>
					<li>민간(대학로) (Private (Daehak-ro))</li>
					<li>공공(문예회관) (Public (Cultural Center))</li>
					<li>기타(비공연장) (Other (Non-Performance Venue))</li>
					<li>공공(기타) (Public (Other))</li>
					<li>국립 (National)</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'location'}
		<div in:fade class="mt-4">
			<img
				src="/images/Region_Counts_Cancellation_Rates.png"
				alt="Region Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 지역의 공연수를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				서울이 공연수에서 압도적으로 많은 것을 확인할 수 있으며, 취소율도 상대적으로 높습니다.
				제주도의 경우 공연수도 많지 않고 취소율도 낮은 편이었습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'paymentMethod'}
		<div in:fade class="mt-4">
			<img
				src="/images/Payment_Method_Counts_Cancellation_Rates.png"
				alt="Payment Method Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 결제수단의 사용빈도를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				많은 관객들이 카드 결제를 선호하는 것을 확인할 수 있으며, 상품권 결제의 경우 취소율이
				15%까지 떨어지는 경향을 보였습니다.(상품권을 결제 수단으로 사용하는 것은 많지 않지만) 반면,
				다중결제 및 현금 결제의 경우 취소율이 비교적 높았습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 결제수단 목록</p>
				<ul class="list-disc list-inside space-y-1">
					<li>기타 (Other)</li>
					<li>카드 (Card)</li>
					<li>현금 (Cash)</li>
					<li>다중결제 (Multiple Payment)</li>
					<li>무통장 (Bank Transfer)</li>
					<li>상품권 (Gift Certificate)</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'discountType'}
		<div in:fade class="mt-4">
			<img
				src="/images/Discount_Type_Counts_Cancellation_Rates.png"
				alt="Discount Type Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 할인 유형의 적용빈도를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				신용카드사 할인을 받은 경우 취소율이 0%(8만건 중)임을 확인할 수 있습니다. 그리고 대부분의
				할인종류가 '기타'로 분류되어 어떤 기준으로 할인종류를 받았는지 특수한 패턴을 찾을 수
				없었습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 할인종류 목록</p>
				<ul class="list-disc list-inside space-y-1">
					<li>기타 (Other)</li>
					<li>자체할인 (In-house Discount)</li>
					<li>미적용 (No Discount)</li>
					<li>신용카드사 (Credit Card Company)</li>
					<li>다중할인 (Multiple Discounts)</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'childPerformance'}
		<div in:fade class="mt-4">
			<img
				src="/images/Child_Performance_Counts_Cancellation_Rates.png"
				alt="Child Performance Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 아동공연 여부에 따른 공연수를, 선그래프는 취소율을 나타냅니다. <br /><br />

				아동공연인 경우 취소율이 약 5% 정도 낮은 경향을 보이고 있습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'performanceDate'}
		<div in:fade class="mt-4">
			<!-- <img
				src="/images/Date_Weather_Boxplot.png"
				alt="Date and Weather Boxplot"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
				style="max-width: 50%;"
			/> -->
			<img
				src="/images/Cancellations_Date_Weather.png"
				alt="Cancellations by Date and Weather"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				이 그래프는 공연일시(Year, Month, Day, Hour, Minute, Weekday), 날씨(온도, 기상환경)와
				취소수간의 관계냅니다. <br />
				날씨는 기상청 공공 api를 활용해서 공연일시에 해당하는 온도와 기상환경을 가져올 수 있었습니다.
				서울지역에 대한 분석이며, 취소수와 다른 변수와의 상관관계가 크지 않은 가운데 공연시간(아래) 그리고
				날씨(다음 페이지)와의 연관성을 추가로 분석하였습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 용어 설명</p>
				<ul class="list-disc list-inside space-y-1">
					<li>avgTm: 평균 온도(0 - 1로 스케일링)</li>
					<li>
						Weather: 기상 현상, 순서대로 0(맑음), 0.2(기타), 0.4(안개), 0.6(황사), 0.8(눈), 1(비)
					</li>
					<li>Weekdays: 요일, 순서대로 월화수목금토일</li>
				</ul>
			</div>
			<br /><br />
			<!-- <img
				src="/images/corrMatrix_Cancellations_Date_Weather.png"
				alt="Correlation Matrix of Cancellations, Date, and Weather"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
				style="max-width: 50%;"
			/> -->
			<img
				src="/images/Hourly_Counts_Cancellation_Rates.png"
				alt="Hourly Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				이 그래프는 공연시간과 취소율간의 관계입니다. <br /> <br />
				14시 공연의 취소율이 상대적으로 약간 높은 편이지만 일반적으로 취소율과 시간사이의 큰 연관성을
				찾을 수 없었습니다. 14시와 19시 시간대의 공연이 가장 많은 점을 확인할 수 있습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'weather'}
		<div in:fade class="mt-4">
			<img
				src="/images/Weather_Cancellation_Rates.png"
				alt="Weather and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 날씨 조건의 빈도를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				날씨에 따라 급격하게 취소율이 변동하는 등의 사실은 확인할 수 없었으나, 눈이 오는 날에는
				취소율이 약간 상승하는 경향이 있었습니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 날씨 목록</p>
				<ul class="list-disc list-inside space-y-1">
					<li>맑음 (Clear)</li>
					<li>비 (Rain)</li>
					<li>눈 (Snow)</li>
					<li>안개 (Fog)</li>
					<li>황사 (Dust)</li>
					<li>기타 (Other)</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'gender'}
		<div in:fade class="mt-4">
			<img
				src="/images/Gender_Cancellation_Rates.png"
				alt="Gender and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 성별 그룹의 크기를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				특정 성별의 차이가 크지 않으나, Gender1의 경우 취소율이 약간 낮은 편입니다.
			</p>
			<div class="bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-2">참고: 성별 구분</p>
				<ul class="list-disc list-inside space-y-1">
					<li>Gender0, Gender1, Gender2 원본데이터 셋 구분에 따른 기준</li>
				</ul>
			</div>
		</div>
	{/if}

	{#if analysisType === 'age'}
		<div in:fade class="mt-4">
			<img
				src="/images/Age_Cancellation_Rates.png"
				alt="Age and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 연령대 분포를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				20대 후반부터 40대 초반까지의 취소율이 25% 정도로 일관성 있는 모습을 점을 확인할 수 있으며,
				30대에서 약간 취소율이 상승하는 경향(가장 공연을 많이 보는 나이대)을 보이다가 40대에서는
				다시 감소하는 경향이 있습니다. 연령대가 극단적으로 높거나 낮아질 경우 취소율이 불안정해지는
				경향이 있었습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'openingYear'}
		<div in:fade class="mt-4">
			<img
				src="/images/Opening_Year_Cancellation_Rates.png"
				alt="Opening Year and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				막대그래프는 각 개관연도별 시설수를, 선그래프는 취소율의 추이를 나타냅니다. <br /><br />

				개관연도가 1620년인 경우를 제외하고, 개관이 오래된 경우에도 취소율이 높지 않은 점을 확인할
				수 있으며, 오히려 개관연도가 최근일 수록 취소율이 조금씩 상승하는 경향을 보였습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'discountAmount'}
		<div in:fade class="mt-4">
			<img
				src="/images/Distribution_of_Discount_Amount.png"
				alt="Distribution of Discount Amount"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
				style="max-width: 50%;"
			/>
			<p class="mb-4">
				위 그래프는 할인금액이 어떻게 분포하는지를 나타내며, 할인 금액이 0인 경우가 압도적으로
				많았습니다.
			</p>
			<br /><br />
			<img
				src="/images/Cancellation_Rate_by_Discount_Amount.png"
				alt="Cancellation Rate by Discount Amount"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				위 그래프는 할인금액에 따른 취소율을 나타냅니다.
				<br /><br />
				대체적으로 할인금액이 커지면서 취소율이 완만히 낮아지는 경향을 보이고 있습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'ticketPrice'}
		<div in:fade class="mt-4">
			<img
				src="/images/Distribution_of_Ticket_Price.png"
				alt="Distribution of Ticket Price"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
				style="max-width: 50%;"
			/>
			<p class="mb-4">
				위 그래프는 장당금액이 어떻게 분포하는지를 나타냅니다. 이상치를 제외하면 0원에서 20만원
				사이에서 가격이 형성됨을 확인할 수 있었습니다.
			</p>
			<img
				src="/images/Cancellation_Rate_by_Ticket_Price.png"
				alt="Cancellation Rate by Ticket Price"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p class="mb-4">
				위 그래프는 티켓 가격에 따른 취소율을 나타냅니다.
				<br /><br />

				티켓 가격이 높아질수록 취소율이 상승하는 경향을 보이고 있는데, 10만원 이상의 경우 그래프의
				변동성이 아래 위로 커지는 경향을 보였습니다.
			</p>
		</div>
	{/if}
</main>
