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
			<p>
				공연 장르에 따른 취소율 분석 결과, 뮤지컬(Musical) 장르가 가장 많았고, 대중무용(Pop Dance)의
				경우 장르 자체의 숫자에 비해 취소율이 높은 부분이 확인되었습니다.
			</p>
			<p>
				뮤지컬 (Musical), 대중음악 (Pop Music), 연극 (Play), 서양음악(클래식) (Western Music
				(Classical)), 무용(서양/한국무용) (Dance (Western/Korean)), 한국음악(국악) (Korean Music
				(Traditional)), 서커스/마술 (Circus/Magic), 복합 (Mixed), 대중무용 (Pop Dance)
			</p>
		</div>
	{/if}

	{#if analysisType === 'facility'}
		<div in:fade class="mt-4">
			<img
				src="/images/Facility_Counts_Cancellation_Rates.png"
				alt="Facility Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				시설 특성에 따른 취소율 분석에서는 민간(대학로 외)(Private/Outside Daehak-ro) 시설이 가장
				많은 공연수를 기록했으며, 취소율도 높았습니다. 반면, 공공(문예회관)(Public/Cultural
				Center)의 경우 공연 수는 많지만 취소율은 상대적으로 낮았습니다.
			</p>
			<p>
				민간(대학로 외) (Private (Outside Daehak-ro)), 민간(대학로) (Private (Daehak-ro)),
				공공(문예회관) (Public (Cultural Center)), 기타(비공연장) (Other (Non-Performance Venue)),
				공공(기타) (Public (Other)), 국립 (National)
			</p>
		</div>
	{/if}

	{#if analysisType === 'location'}
		<div in:fade class="mt-4">
			<img
				src="/images/Region_Counts_Cancellation_Rates.png"
				alt="Region Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				공연 지역별 취소율 분석에서는 서울이 공연 수에서 압도적으로 많았으며, 취소율도 높은 것으로
				나타났습니다. 제주도의 경우 비율상 가장 낮은 취소율을 보였습니다.
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
			<p>
				결제수단별 취소율 분석에서는 카드(Card) 결제가 과반수를 차지했으며, 상품권(Gift Certificate)
				결제의 경우 취소율이 15%까지 떨어지는 경향을 보였습니다. 다중결제(Multiple Payment) 및
				현금(Cash) 결제의 경우 취소율이 비교적 높았습니다.
			</p>
			<p>
				기타 (Other), 카드 (Card), 현금 (Cash), 다중결제 (Multiple Payment), 무통장 (Bank Transfer),
				상품권 (Gift Certificate)
			</p>
		</div>
	{/if}

	{#if analysisType === 'discountType'}
		<div in:fade class="mt-4">
			<img
				src="/images/Discount_Type_Counts_Cancellation_Rates.png"
				alt="Discount Type Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				할인종류별 취소율 분석에서는 신용카드사(Credit Card Company) 할인을 받은 경우 취소율이 0%로
				나타났습니다. 기타 할인종류는 대부분 기타(Other)로 분류되어 데이터 신뢰성이 낮았습니다.
			</p>
			<p>
				기타 (Other), 자체할인 (In-house Discount), 미적용 (No Discount), 신용카드사 (Credit Card
				Company), 다중할인 (Multiple Discounts)
			</p>
		</div>
	{/if}

	{#if analysisType === 'childPerformance'}
		<div in:fade class="mt-4">
			<img
				src="/images/Child_Performance_Counts_Cancellation_Rates.png"
				alt="Child Performance Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>아동공연인 경우가 아닌 경우보다 취소율이 약 5% 정도 낮은 경향을 보였습니다.</p>
		</div>
	{/if}

	{#if analysisType === 'performanceDate'}
		<div in:fade class="mt-4">
			<img
				src="/images/Date_Weather_Boxplot.png"
				alt="Date and Weather Boxplot"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<img
				src="/images/Cancellations_Date_Weather.png"
				alt="Cancellations by Date and Weather"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<img
				src="/images/corrMatrix_Cancellations_Date_Weather.png"
				alt="Correlation Matrix of Cancellations, Date, and Weather"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<img
				src="/images/Hourly_Counts_Cancellation_Rates.png"
				alt="Hourly Counts and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				공연일시에 따른 취소율 분석에서는 14시 공연의 취소율이 상대적으로 높은 편이며, 시간대 자체는
				14시와 19시 공연이 가장 많았습니다. 날씨와의 관련성은 크지 않았습니다.
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
			<p>
				날씨에 따른 취소율 분석에서는 날씨와 취소율의 관계가 거의 없었으나, 눈이 오는 날에 취소율이
				약간 상승하는 경향이 있었습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'gender'}
		<div in:fade class="mt-4">
			<img
				src="/images/Gender_Cancellation_Rates.png"
				alt="Gender and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				성별에 따른 취소율 분석에서는 특정 성별의 차이가 크지 않으나, Gender1의 경우 취소율이 약간
				낮은 편입니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'age'}
		<div in:fade class="mt-4">
			<img
				src="/images/Age_Cancellation_Rates.png"
				alt="Age and Cancellation Rates"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				연령에 따른 취소율 분석에서는 20대 후반부터 40대 초반까지의 취소율이 25% 정도로 나타났으며,
				연령대가 극단적으로 높거나 낮아질 경우 취소율이 불안정해지는 경향이 있었습니다.
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
			<p>
				개관연도에 따른 취소율 분석에서는 개관연도가 오래된 경우에도 취소율이 높지 않았으며,
				1997년에 개관한 시설에서 취소율이 5%로 낮게 나타난 예를 확인할 수 있었습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'discountAmount'}
		<div in:fade class="mt-4">
			<img
				src="/images/Distribution_of_Discount_Amount.png"
				alt="Distribution of Discount Amount"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<img
				src="/images/Cancellation_Rate_by_Discount_Amount.png"
				alt="Cancellation Rate by Discount Amount"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				할인금액에 따른 취소율 분석에서는 할인금액이 커지면 취소율이 낮아지는 경향을 보였습니다.
				대부분의 경우 할인금액이 0원인 경우가 많았습니다.
			</p>
		</div>
	{/if}

	{#if analysisType === 'ticketPrice'}
		<div in:fade class="mt-4">
			<img
				src="/images/Distribution_of_Ticket_Price.png"
				alt="Distribution of Ticket Price"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<img
				src="/images/Cancellation_Rate_by_Ticket_Price.png"
				alt="Cancellation Rate by Ticket Price"
				class="w-full h-auto object-contain rounded-lg border border-gray-300 mb-4"
			/>
			<p>
				장당금액에 따른 취소율 분석에서는 티켓 가격이 높아질수록 취소율도 높아지는 경향이
				나타났습니다. 특히 10만원 이상의 경우 그래프의 움직임이 커지는 모습을 보였습니다.
			</p>
		</div>
	{/if}
</main>
