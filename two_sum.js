function twoSum(nums, target) {
    const seen = new Map();

    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];

        if (seen.has (complement)) {
            return [seen.get(complement), i];

        }

        seen.set(nums[i], i);

        }

        return [];
    }

    const nums = [2, 7, 11, 15];
    const target = 9;
    
    console.log("Numbers:", nums);
    console.log("Target:", target);
    console.log("Answer:", twoSum(nums,target));
