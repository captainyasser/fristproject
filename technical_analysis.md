# تفاصيل آلية تحديث القوائم (Frontend Logic)

## المشكلة السابقة
كانت القوائم تعتمد على إخفاء/إظهار عناصر `option` الموجودة مسبقاً في `DOM`. هذه الطريقة تسبب مشاكل مع مكتبة `Select2` التي تقوم بإنشاء عناصر DOM خاصة بها، مما يؤدي إلى عدم تزامن العرض مع البيانات الفعلية، وتأخير في الاستجابة (Race Conditions).

## الحل المطبق (Re-render Strategy)
تم تغيير الاستراتيجية بالكامل لتعتمد على **إعادة بناء القوائم (Re-render)** بناءً على "مصدر حقيقة" (Single Source of Truth) يأتي من السيرفر كبيانات خام (JSON).

### 1. البيانات (The Data)
يتم تمرير البيانات التالية من الـ `View` (Backend) إلى الـ `Template` بصيغة JSON String:
- `violationTypes`: قائمة أنواع المخالفات.
- `penaltyAppliedList`: قائمة الجزاءات الموقعة (تحتوي على `penalty_level_id`).
- `penaltyLevels`: قائمة أنواع الجزاءات (للمرجع).

يتم استقبالها في الجافاسكريبت كالكائنات التالية:
```javascript
const violationTypes = JSON.parse('{{ violation_types|escapejs }}');
const penaltyAppliedList = JSON.parse('{{ penalty_applied_list|escapejs }}');
const penaltyLevels = JSON.parse('{{ penalty_levels|escapejs }}');
```

### 2. دالة التحديث العامة (`renderOptions`)
تم إنشاء دالة مساعدة تقوم بمهام محددة لضمان الاستقرار:
1.  تفريغ القائمة الحالية (`empty()`).
2.  إضافة خيار افتراضي (Placeholder).
3.  المرور على البيانات الخام وإضافة العناصر التي تطابق شرط الفلترة (`filterFn`).
4.  **إعادة تحديد القيمة المختارة سابقاً** إذا كانت لا تزال صالحة ضمن القائمة الجديدة.
5.  تحديث واجهة `Select2` (`trigger('change.select2')`).

### 3. السيناريوهات (Scenarios)

#### أ. عند تغيير "الجزاء الموقع" (Applied Penalty)
*الهدف*: تحديد "نوع الجزاء" (Penalty Level) تلقائياً.
*الكود*:
```javascript
appliedSelect.on('select2:select', function(e){
    const appliedId = $(this).val();
    const meta = penaltyAppliedList.find(x => x.id == appliedId);
    if(meta) {
        // نقوم بتحديث نوع الجزاء مباشرةً بالقيمة المرتبطة
        levelSelect.val(meta.penalty_level_id).trigger('change.select2');
    }
});
```
*ملاحظة*: هذا التغيير سيؤدي تلقائياً إلى تشغيل السيناريو (ب) لأننا أطلقنا حدث `change.select2`.

#### ب. عند تغيير "نوع الجزاء" (Penalty Level)
*الهدف*: فلترة قائمة "الجزاءات الموقعة" لتظهر فقط ما يتناسب مع النوع المختار.
*الكود*:
```javascript
levelSelect.on('change select2:select', function(e){
     updateAppliedOptions();
});

function updateAppliedOptions() {
    const levelId = levelSelect.val();
    // إعادة بناء القائمة بناءً على الـ levelId المختار
    renderOptions(appliedSelect, penaltyAppliedList, 'id', 'name', 
        (item) => !levelId || item.penalty_level_id == levelId
    );
}
```

### نقاط للمراجعة (Debugging)
إذا لم تعمل الكود كما هو متوقع، يرجى التحقق من التالي:
1.  **Select2 Events**: تأكد من أن المكتبة لا تمنع انتشار الأحداث. الكود الحالي يستمع لـ `select2:select` (اختيار المستخدم) و `change` (تغيير برمجي).
2.  **Data Types**: تأكد من أن `id` القادم من السيرفر (Integer) يتم مقارنته بشكل صحيح مع `val()` القادم من القائمة (عادة String). الدالة تستخدم `==` (ليس `===`) لتجاوز هذه المشكلة.
3.  **Console Errors**: افتح الـ Console وتأكد من عدم وجود أخطاء في `JSON.parse`.

هذا النظام يضمن أن القائمة المعروضة دائماً متطابقة مع البيانات المسموح بها، "لحظياً" وبدون تعارضات.
