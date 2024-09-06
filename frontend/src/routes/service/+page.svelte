<!-- frontend/src/routes/service/+page.svelte -->

<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import CancellationGraph from '$lib/CancellationGraph.svelte';
	import { fade } from 'svelte/transition';

	let eventCode = '';
	let cancellationData = [];
	let timePoints = {};
	let isLoading = true;
	let error = null;
	let showGraph = writable(false);

	const API_URL = import.meta.env.VITE_API_URL;

	function handleEventCodeChange(event) {
		const selectedValue = event.target.value;

		if (selectedValue === 'eventCode1') {
			eventCode = 'PF343804';
		} else if (selectedValue === 'eventCode2') {
			eventCode = 'PF352013';
		} else if (selectedValue === 'eventCode3') {
			eventCode = 'PF392163';
		}
		resetFields();
	}

	let eventDate = '';
	let discountAmount = '';
	let pricePerTicket = '';
	let gender = {
		gender_1: undefined,
		gender_2: undefined,
		gender_0: undefined
	};
	let age = '';
	let paymentDetails = {
		cardPayment: undefined,
		otherPayment: undefined,
		bankTransfer: undefined,
		multiplePayments: undefined,
		cashPayment: undefined,
		voucherPayment: undefined
	};
	let discountDetails = {
		otherDiscount: undefined,
		selfDiscount: undefined
	};

	let predictedCancellationCount = writable<number | null>(null);
	let flaskMessage: string = '';

	let predictedCount: number | null;
	$: predictedCount = $predictedCancellationCount;
	let predictedRemainingSeats: number | null = null;

	let eventImages = {
		PF343804: '/images/PF343804.jpeg',
		PF352013: '/images/PF352013.jpg',
		PF392163: '/images/PF392163.jpg'
	};

	let selectedImageUrl: string | null = null;
	$: selectedImageUrl = eventCode ? eventImages[eventCode] : null;
	$: console.log('Data for graph:', cancellationData, timePoints);
	$: eventCode && fetchCancellationData();

	async function fetchCancellationData() {
		if (!eventCode) return;

		isLoading = true;
		try {
			const response = await fetch(`${API_URL}/cancellation-data?eventCode=${eventCode}`);
			if (!response.ok) {
				throw new Error('Failed to fetch cancellation data');
			}
			const data = await response.json();

			// Log the received data
			console.log('Received data:', data);

			if (data.error) {
				throw new Error(data.error);
			}
			cancellationData = data.data;
			timePoints = data.timePoints;
		} catch (err) {
			error = err.message;
		} finally {
			isLoading = false;
		}
	}

	onMount(async () => {
		if (eventCode) {
			fetchCancellationData();
		}
		if (!eventCode) {
			flaskMessage = 'Error: Event code not selected';
			isLoading = false;
			return;
		}

		try {
			const response = await fetch(`/api/cancellation-data?eventCode=${eventCode}`);
			if (!response.ok) {
				throw new Error('Failed to fetch cancellation data');
			}
			const data = await response.json();
			if (data.error) {
				throw new Error(data.error);
			}
			cancellationData = data.data;
			timePoints = data.timePoints;

			console.log('Cancellation Data:', cancellationData);
			console.log('Time Points:', timePoints);
		} catch (error) {
			flaskMessage = 'Error: ' + error.message;
		} finally {
			isLoading = false;
		}
	});

	let showAnalysisButton = writable(false);
	let showAnalysis = writable(false);

	async function predictCancellation() {
		const data = {
			eventCode,
			eventDate,
			discountAmount,
			pricePerTicket,
			gender,
			age,
			paymentDetails,
			discountDetails
		};

		try {
			const response = await fetch(`${API_URL}/predict`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			});

			if (response.ok) {
				const result = await response.json();
				predictedCancellationCount.set(result.predictedCancellationCount);
				predictedRemainingSeats = result.predictedRemainingSeats;
				showAnalysisButton.set(true);
				await fetchCancellationData(); // 예측 후 데이터 로드하여 그래프 표시
				showGraph.set(true); // 그래프 표시
			} else {
				flaskMessage = 'Failed to load prediction';
			}
		} catch (error) {
			flaskMessage = 'Error: ' + error.message;
		}
	}

	function resetFields() {
		eventDate = '';
		discountAmount = '';
		pricePerTicket = '';
		gender = {
			gender_1: undefined,
			gender_2: undefined,
			gender_0: undefined
		};
		age = '';
		paymentDetails = {
			cardPayment: undefined,
			otherPayment: undefined,
			bankTransfer: undefined,
			multiplePayments: undefined,
			cashPayment: undefined,
			voucherPayment: undefined
		};
		discountDetails = {
			otherDiscount: undefined,
			selfDiscount: undefined
		};
		predictedCancellationCount.set(null);
		selectedImageUrl = eventCode ? eventImages[eventCode] : null;
		predictedRemainingSeats = null;
		showAnalysisButton.set(false);
		showAnalysis.set(false);
		showGraph.set(false);
	}
</script>

<main class="w-full max-w-[850px] mx-auto p-4 relative">
	<div class="relative">
		<h1 class="text-2xl font-bold mb-4">
			공연 취소
			<span class="text-[#696969]"> 예측 </span>
			서비스
		</h1>

		{#if selectedImageUrl}
			<div
				class="absolute top-0 left-[400px] w-32 h-32 z-10"
				in:fade={{ duration: 150, delay: 100 }}
				out:fade={{ duration: 150 }}
			>
				<img
					src={selectedImageUrl}
					alt=""
					class="w-full h-full object-cover rounded-lg border border-gray-300"
				/>
			</div>
		{/if}
	</div>

	{#if !$showAnalysis}
		<div class="mt-8">
			<h2 class="text-l font-semibold mb-2">공연코드 선택</h2>
			<div class="flex items-center gap-4">
				<div
					class="w-[328px] h-12 pl-4 pr-2 py-2 bg-white rounded-lg border border-[#121212]/10 justify-start items-center gap-2 inline-flex"
				>
					<select
						id="eventCode"
						bind:value={eventCode}
						on:change={handleEventCodeChange}
						class="w-full text-[#121212]/40 text-sm font-normal tracking-wide bg-transparent border-none focus:outline-none"
						style="font-family: 'Noto Sans KR', sans-serif;"
						required
					>
						<option value="" disabled selected>공연코드 선택</option>
						<option value="PF343804">PF343804</option>
						<option value="PF352013">PF352013</option>
						<option value="PF392163">PF392163</option>
					</select>
				</div>
			</div>
		</div>
		<br />

		{#if eventCode}
			<form
				on:submit|preventDefault={predictCancellation}
				in:fade={{ duration: 200 }}
				out:fade={{ duration: 200 }}
			>
				<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
					<!-- 기본 정보 -->
					<div class="bg-gray-100 p-6 rounded-lg shadow">
						<h3 class="text-lg font-semibold mb-4">기본 정보</h3>
						<div class="space-y-4">
							<div class="flex flex-col">
								<label for="eventCode" class="text-sm font-medium text-gray-700 mb-1"
									>공연코드</label
								>
								<input
									type="text"
									id="eventCode"
									bind:value={eventCode}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="공연코드"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="eventDate" class="text-sm font-medium text-gray-700 mb-1"
									>공연일시</label
								>
								<input
									type="datetime-local"
									id="eventDate"
									bind:value={eventDate}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									required
								/>
							</div>
						</div>
					</div>

					<!-- 가격 정보 -->
					<div class="bg-gray-100 p-6 rounded-lg shadow">
						<h3 class="text-lg font-semibold mb-4">가격 정보</h3>
						<div class="space-y-4">
							<div class="flex flex-col">
								<label for="discountAmount" class="text-sm font-medium text-gray-700 mb-1"
									>평균 할인금액</label
								>
								<input
									type="number"
									id="discountAmount"
									bind:value={discountAmount}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="각 관객이 받은 할인금액의 평균값 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="pricePerTicket" class="text-sm font-medium text-gray-700 mb-1"
									>평균 장당금액</label
								>
								<input
									type="number"
									id="pricePerTicket"
									bind:value={pricePerTicket}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="각 관객이 지불한 장당금액의 평균"
									step="0.01"
									required
								/>
							</div>
						</div>
					</div>

					<!-- 성별 및 연령 정보 -->
					<div class="bg-gray-100 p-6 rounded-lg shadow">
						<h3 class="text-lg font-semibold mb-4">성별 및 연령 정보</h3>
						<div class="space-y-4">
							<div class="flex flex-col">
								<label for="gender_1" class="text-sm font-medium text-gray-700 mb-1"
									>gender_1 인원수</label
								>
								<input
									type="number"
									id="gender_1"
									bind:value={gender.gender_1}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="gender1 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="gender_2" class="text-sm font-medium text-gray-700 mb-1"
									>gender_2 인원수</label
								>
								<input
									type="number"
									id="gender_2"
									bind:value={gender.gender_2}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="gender2 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="gender_0" class="text-sm font-medium text-gray-700 mb-1"
									>gender_0 인원수</label
								>
								<input
									type="number"
									id="gender_0"
									bind:value={gender.gender_0}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="gender0 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="age" class="text-sm font-medium text-gray-700 mb-1">연령 평균</label>
								<input
									type="number"
									id="age"
									bind:value={age}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="예매한 모든 관객의 연령 평균"
									step="0.01"
									required
								/>
							</div>
						</div>
					</div>

					<!-- 결제 방법 -->
					<div class="bg-gray-100 p-6 rounded-lg shadow">
						<h3 class="text-lg font-semibold mb-4">결제 방법</h3>
						<div class="space-y-4">
							<div class="flex flex-col">
								<label for="cardPayment" class="text-sm font-medium text-gray-700 mb-1"
									>카드 결제 인원</label
								>
								<input
									type="number"
									id="cardPayment"
									bind:value={paymentDetails.cardPayment}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="카드로 결제한 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="otherPayment" class="text-sm font-medium text-gray-700 mb-1"
									>기타 결제 인원</label
								>
								<input
									type="number"
									id="otherPayment"
									bind:value={paymentDetails.otherPayment}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="기타 방법으로 결제한 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="bankTransfer" class="text-sm font-medium text-gray-700 mb-1"
									>무통장 결제 인원</label
								>
								<input
									type="number"
									id="bankTransfer"
									bind:value={paymentDetails.bankTransfer}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="무통장으로 결제한 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="multiplePayments" class="text-sm font-medium text-gray-700 mb-1"
									>다중 결제 인원</label
								>
								<input
									type="number"
									id="multiplePayments"
									bind:value={paymentDetails.multiplePayments}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="다중 결제 방식으로 결제한 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="cashPayment" class="text-sm font-medium text-gray-700 mb-1"
									>현금 결제 인원</label
								>
								<input
									type="number"
									id="cashPayment"
									bind:value={paymentDetails.cashPayment}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="현금으로 결제한 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							{#if eventCode === 'PF392163'}
								<div class="flex flex-col">
									<label for="voucherPayment" class="text-sm font-medium text-gray-700 mb-1"
										>상품권 결제 인원</label
									>
									<input
										type="number"
										id="voucherPayment"
										bind:value={paymentDetails.voucherPayment}
										class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
										placeholder="상품권으로 결제한 인원수 입력"
										step="0.01"
										required
									/>
								</div>
							{/if}
						</div>
					</div>

					<!-- 할인 정보 -->
					<div class="bg-gray-100 p-6 rounded-lg shadow">
						<h3 class="text-lg font-semibold mb-4">할인 정보</h3>
						<div class="space-y-4">
							<div class="flex flex-col">
								<label for="otherDiscount" class="text-sm font-medium text-gray-700 mb-1"
									>기타 할인 인원</label
								>
								<input
									type="number"
									id="otherDiscount"
									bind:value={discountDetails.otherDiscount}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="기타 방법으로 할인 받은 인원수 입력"
									step="0.01"
									required
								/>
							</div>
							<div class="flex flex-col">
								<label for="selfDiscount" class="text-sm font-medium text-gray-700 mb-1"
									>자체 할인 인원</label
								>
								<input
									type="number"
									id="selfDiscount"
									bind:value={discountDetails.selfDiscount}
									class="text-sm w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
									placeholder="자체 할인 방법으로 할인 받은 인원수 입력"
									step="0.01"
									required
								/>
							</div>
						</div>
					</div>
				</div>
				<div class="h-[120px] flex justify-start items-center gap-4 mt-4">
					<div class="h-14 p-3 bg-[#050a11] rounded-lg flex justify-center items-center gap-2">
						<button
							type="submit"
							class="text-white text-sm font-semibold font-['Poppins'] tracking-wide"
							style="font-family: 'Noto Sans KR', sans-serif;"
						>
							예측하기
						</button>
					</div>
					<div class="h-14 p-3 bg-[#d1d5db] rounded-lg flex justify-center items-center gap-2">
						<button
							type="button"
							on:click={resetFields}
							class="text-black text-sm font-semibold font-['Poppins'] tracking-wide"
							style="font-family: 'Noto Sans KR', sans-serif;"
						>
							다시하기
						</button>
					</div>
					{#if $showAnalysisButton}
						<div class="h-14 p-3 bg-[#4b5563] rounded-lg flex justify-center items-center gap-2">
							<button
								type="button"
								on:click={() => showAnalysis.set(true)}
								class="text-white text-sm font-semibold font-['Poppins'] tracking-wide"
								style="font-family: 'Noto Sans KR', sans-serif;"
							>
								분석결과
							</button>
						</div>
					{:else}
						<!-- svelte-ignore empty-block -->
					{/if}
				</div>
			</form>
		{/if}
	{/if}

	{#if eventCode}
		<div class="mt-4">
			<div class="flex items-center gap-4">
				<div class="h-14 p-3 bg-white rounded-lg border border-gray-300 flex items-center">
					<h2 class="text-sm font-semibold">취소표 개수 예측</h2>
				</div>
				<div class="h-14 p-3 bg-white flex items-center">
					<p class="text-sm text-gray-700">
						{#if predictedCount !== null}
							{predictedCount}
						{:else}{/if}
					</p>
				</div>
			</div>
			<div class="flex items-center gap-4 mt-4">
				<div class="h-14 p-3 bg-white rounded-lg border border-gray-300 flex items-center">
					<h2 class="text-sm font-semibold">남은 좌석수 예측</h2>
				</div>
				<div class="h-14 p-3 bg-white flex items-center">
					<p class="text-sm text-gray-700">
						{#if predictedRemainingSeats !== null}
							{predictedRemainingSeats}
						{:else}{/if}
					</p>
				</div>
			</div>
		</div>
		<br />
		<div class="mt-8 text-center">
			{#if isLoading}
				<p class="text-gray-600">Loading...</p>
			{:else if error}
				<p class="text-red-600">Error: {error}</p>
			{:else if cancellationData.length > 0 && !$showAnalysis}
				{#if $showGraph}
					<div class="w-full h-[300px] sm:h-[400px] md:h-[500px] lg:h-[600px]">
						<CancellationGraph data={cancellationData} {timePoints} />
					</div>
				{/if}
			{/if}
		</div>
	{/if}

	{#if $showAnalysis}
		<div class="mt-8">
			<h2 class="text-l font-semibold mb-2">{eventCode} 분석결과</h2>
			<div class="mt-4 p-6 text-sm text-gray-700 leading-relaxed shadow-md rounded-lg">
				<ul class="space-y-2">
					<p>
						다음은 공연별 데이터 분석 결과에 대한 설명입니다. 이 분석은 동일한 공연장, 공연 코드,
						공연 일시를 기준으로 그룹화한 데이터프레임을 사용하여 진행했습니다. 분석에 사용된 특성은
						공연 주최측이 어떤 데이터를 주로 활용할 수 있는지, 중복되는 데이터가 많은지 그리고 특정
						특성이 예측의 정확성에 얼마나 영향을 미치는지를 고려했습니다. 참고로, 날씨 데이터는 예측
						정확성에 큰 영향을 미치지 않기 때문에 제외되었습니다.
					</p>
					<br />
					<p>
						모델의 성능은 평균 제곱근 오차(RMSE)와 결정계수(R2 score)로 평가했습니다. RMSE는 예측
						값과 실제 값 사이의 차이를 나타내며, 값이 낮을수록 좋습니다. 반면, R2 score는 모델이
						데이터의 변동성을 얼마나 잘 설명하는지를 나타내며, 1에 가까울수록 성능이 우수하다고
						평가할 수 있습니다. 두 평가지표는 각각 예측 오차(RMSE)와 설명력(R2 score)을 측정하여,
						모델이 예측을 잘하면서도 데이터의 변동성을 잘 설명하는지를 종합적으로 평가하기 때문에
						상호보완적인 역할을 합니다.
					</p>
				</ul>
			</div>

			{#if eventCode === 'PF343804'}
				<div class="mt-8 space-y-8">
					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/343804_c.png"
							alt="특징 vs 취소 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF343804에서 취소수와 여러 특징 간의 관계를 보여줍니다. <br />
							그래프는 취소수와의 상관관계 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Cancellations: 취소수</li>
								<li>Discount_Type_Other: 기타 할인수</li>
								<li>Payment_Method_Other: 기타 결제수</li>
								<li>Payment_Method_Card: 카드 결제수</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/343804_r.png"
							alt="특징 vs 남은 좌석 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF343804에서 남은 좌석수와 여러 특징 간의 관계를 보여줍니다.<br
							/>
							그래프는 해당 특징과 남은 좌석수 사이의 상관관계가 높은 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Remaining: 남은 좌석수</li>
								<li>Discount_Type_Other: 기타 할인수</li>
								<li>Payment_Method_Cash: 현금 결제수</li>
								<li>Avg_Discount: 평균 할인 금액</li>
								<li>Payment_Method_Bank: 무통장 입금수</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/343804_RF_c.png"
							alt="XGBoost 특징 중요도 (취소)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							이 그래프는 예측에 사용된 XGBoost 모델에서 취소수 예측에 가장 큰 영향을 미친 특징들을
							보여줍니다. <br /> 각 막대의 길이는 취소수 예측에 사용된 특징의 중요도를 나타냅니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 8.15</li>
								<li>결정계수(R2 score): 0.95</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/343804_RF_r.png"
							alt="랜덤포레스트 특징 중요도 (남은 좌석 수)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 남은 좌석수 예측에 사용된 랜덤포레스트 모델에서 예측에 가장 큰 영향을 미친
							특징들을 보여줍니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 23.39</li>
								<li>결정계수(R2 score): 0.89</li>
							</ul>
						</div>
					</div>
				</div>
			{:else if eventCode === 'PF352013'}
				<div class="mt-8 space-y-8">
					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/352013_c.png"
							alt="특징 vs 취소 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF352013에서 취소수와 여러 특징 간 관계를 보여줍니다. <br />
							그래프는 취소수와 특징들의 상관관계 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Cancellations: 취소수</li>
								<li>Payment_Method_Card: 카드 결제수</li>
								<li>Payment_Method_Other: 기타 결제수</li>
								<li>Payment_Method_Bank: 무통장 결제수</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/352013_r.png"
							alt="특징 vs 남은 좌석 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF352013에서 남은 좌석수와 여러 특징 간의 관계를 보여줍니다. <br
							/>
							그래프는 각 특징과 남은 좌석수 사이의 상관관계가 높은 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Remaining: 남은 좌석수</li>
								<li>Avg_Age: 평균 나이</li>
								<li>Avg_Price: 평균 결제 금액</li>
								<li>Payment_Method_Cash: 현금 결제수</li>
								<li>Discount_Type_Other: 기타 할인수</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/352013_XG_c.png"
							alt="XGBoost 특징 중요도 (취소)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							이 그래프는 XGBoost 모델에서 취소수 예측에 가장 큰 영향을 미친 특징들을 보여줍니다. <br
							/>
							각 막대의 길이는 해당 특징의 중요도를 나타냅니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 4.69</li>
								<li>결정계수(R2 score): 0.82</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/352013_XG_r.png"
							alt="XGBoost 특징 중요도 (남은 좌석 수)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 XGBoost 모델에서 남은 좌석수 예측에 가장 큰 영향을 미친 특징들을
							보여줍니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 7.84</li>
								<li>결정계수(R2 score): 0.92</li>
							</ul>
						</div>
					</div>
				</div>
			{:else if eventCode === 'PF392163'}
				<div class="mt-8 space-y-8">
					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/392163_c.png"
							alt="특징 vs 취소 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF392163에서 취소수와 여러 특징 간의 관계를 보여줍니다. <br />
							그래프는 특징들과 취소수 사이의 상관관계 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Cancellations: 취소수</li>
								<li>Payment_Method_Card: 카드 결제수</li>
								<li>Payment_Method_Other: 기타 결제수</li>
								<li>Payment_Method_Bank: 무통장 입금수</li>
								<li>Payment_Method_Multi: 다중 결제수</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/392163_r.png"
							alt="특징 vs 남은 좌석 수"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 공연코드 PF392163에서 남은 좌석수와 여러 특징 간의 관계를 보여줍니다.<br
							/>
							그래프는 각 특징과 남은 좌석수 사이의 상관관계가 높은 순서대로 배치되어 있습니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">주요 용어 설명:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>Remaining: 남은 좌석수</li>
								<li>Avg_Price: 티켓의 평균 가격</li>
								<li>Avg_Discount: 평균 할인 금액</li>
								<li>Avg_Age: 예매자의 평균 나이</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/392163_RF_c.png"
							alt="랜덤포레스트 특징 중요도 (취소)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 취소수 예측을 위한 랜덤포레스트 모델에서 예측에 가장 큰 영향을 미친
							특징들을 보여줍니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 3.32</li>
								<li>결정계수(R2 score): 0.74</li>
							</ul>
						</div>
					</div>

					<div class="bg-white p-6 rounded-lg shadow-md">
						<img
							src="/images/392163_RF_r.png"
							alt="랜덤포레스트 특징 중요도 (남은 좌석 수)"
							class="w-full object-contain rounded-lg border border-gray-300 mb-4"
						/>
						<p class="text-sm text-gray-700 leading-relaxed">
							위 그래프는 랜덤포레스트 모델에서 남은 좌석수 예측에 가장 큰 영향을 미친 특징들을
							보여줍니다.
						</p>
						<div class="mt-4 bg-gray-100 p-4 rounded-lg text-sm text-gray-700">
							<p class="font-semibold mb-2">모델 평가:</p>
							<ul class="list-disc list-inside space-y-1">
								<li>평균 제곱근 오차(RMSE): 14.43</li>
								<li>결정계수(R2 score): 0.90</li>
							</ul>
						</div>
					</div>
				</div>
			{/if}

			<div class="mt-8 bg-gray-100 p-6 rounded-lg text-sm text-gray-700">
				<p class="font-semibold mb-4">참고: 주요 용어 설명</p>
				<ul class="list-disc list-inside space-y-2">
					<li>Remaining: 공연의 남은 좌석수로 원본 데이터셋의 좌석수에서 판매좌석수를 뺀 값</li>
					<li>Avg_Discount: 특정 공연의 티켓 할인 금액의 평균</li>
					<li>Avg_Price: 특정 공연의 평균 티켓 가격</li>
					<li>Avg_Age: 예매자의 평균 나이</li>
					<li>
						Gender_0_Count, Gender_1_Count, Gender_2_Count: 성별 카운트(원본 데이터셋의 분류에 따름)
					</li>
					<li>Payment_Method_Card: 카드 결제수</li>
					<li>Payment_Method_Other: 기타 결제수</li>
					<li>Payment_Method_Bank: 무통장 입금수</li>
					<li>Payment_Method_Multi: 다중 결제수</li>
					<li>Payment_Method_Cash: 현금 결제수</li>
					<li>Payment_Method_Certificate: 상품권 결제수</li>
					<li>Discount_Type_Other: 기타 할인 수</li>
					<li>Discount_Type_InHouse: 자체 할인 수</li>
				</ul>
			</div>

			<div
				class="bg-[#050a11] rounded-lg flex justify-center items-center gap-2 mt-4"
				style="width: 100px; height: 50px;"
			>
				<button
					type="button"
					on:click={() => {
						showAnalysis.set(false);
						window.scrollTo({ top: 0, behavior: 'smooth' });
					}}
					class="text-white font-semibold font-['Poppins'] tracking-wide"
					style="font-family: 'Noto Sans KR', sans-serif; font-size: calc(0.3 * 50px);"
				>
					뒤로가기
				</button>
			</div>
		</div>
	{/if}
</main>
