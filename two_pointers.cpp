#include <iostream>
#include <vector>
using namespace std;

bool hasPair(vector<int>& nums, int target) {
    int left = 0;
    int right = nums.size() - 1;

    while (left < right) {
        int sum = nums[left] + nums[right];

        if (sum == target)
            return true;

        if (sum < target)
            left++;
        else
            right--;
    }

    return false;
}

int main() {
    vector<int> nums = {1, 2, 4, 6, 8, 9};
    int target = 10;

    cout << boolalpha << hasPair(nums, target) << endl;
}